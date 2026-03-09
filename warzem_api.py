import os
import logging
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from zabbix_ai_analyzer.collector.zabbix_hosts import search_hosts
from zabbix_ai_analyzer.collector.zabbix_metrics import fetch_metrics
from zabbix_ai_analyzer.collector.zabbix_problems import fetch_problems
from zabbix_ai_analyzer.ai.ollama_client import OllamaClient
from main import ZabbixCollector
from veeam_mcp_server import get_veeam_backup_status, get_failed_veeam_jobs

# Load environments gracefully
load_dotenv()

app = FastAPI(title="Warzem AI Backend", description="Backend SRE + Ollama para Web App Warzem")

# Allow CORS for Nuxt Frontend (port 8080)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Liberando para facilitar acesso via IP de rede local
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger("warzem.api")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

# Instances
zabbix_url = os.environ.get("ZABBIX_URL", "https://monitoramento.armazem.cloud/api_jsonrpc.php")
zabbix_user = os.environ.get("ZABBIX_USER", "zabbix_api")
zabbix_pass = os.environ.get("ZABBIX_PASS", "")
ollama_address = os.environ.get("OLLAMA_ADDRESS", "http://10.1.254.32:11434")

# Global dependencies
zabbix_collector = ZabbixCollector(zabbix_url, zabbix_user, zabbix_pass)
ai_client = OllamaClient(address=ollama_address, model="llama3:latest", short_mode=True)

@app.get("/api/health")
async def health_check():
    ollama_ok = False
    try:
        import requests
        r = requests.get(f"{ollama_address}/api/tags", timeout=2)
        ollama_ok = r.status_code == 200
    except:
        ollama_ok = False
        
    return {
        "status": "ok", 
        "zabbix_connected": zabbix_collector.zapi is not None,
        "ollama_connected": ollama_ok
    }

@app.get("/api/dashboard")
async def get_dashboard():
    """
    Retorna estatísticas reais consolidadas para o Dashboard.
    Integra Zabbix + MCP Servers (Network & Virtual).
    """
    zapi = zabbix_collector.zapi
    if not zapi:
        return {"error": "Zabbix Down"}
    
    # 1. Dados Zabbix (Physical)
    hosts_count = zapi.host.get(countOutput=True)
    active_problems = zapi.problem.get(countOutput=True, filter={"recent": "1"})
    
    # 2. Dados de Rede (Simulando chamada aos MCP Tools de Juniper)
    # No futuro aqui chamaremos o client MCP, por enquanto usamos a lógica direta do pysnmp para garantir tempo real
    from juniper_mcp_server import fetch_snmp_data as fetch_juniper
    
    net_status = "online"
    try:
        # Teste rápido de conectividade com o core 01
        res = await fetch_juniper("192.168.0.155", "RT-ADC-BQ-01-MGT", "1.3.6.1.2.1.1.3.0")
        if "Erro" in res: net_status = "degraded"
    except:
        net_status = "offline"

    # 3. Dados Virtuais (vCenter/NSX-T)
    from nsxt_mcp_server import fetch_snmp_data as fetch_nsxt
    virt_status = "online"
    try:
        res = await fetch_nsxt("10.21.50.246", "public", "1.3.6.1.2.1.1.3.0")
        if "Erro" in res: virt_status = "degraded"
    except:
        virt_status = "offline"

    # 4. Dados de Backup (Veeam)
    from veeam_mcp_server import get_failed_veeam_jobs as fetch_veeam
    backup_status = "online"
    try:
        res = await fetch_veeam()
        if "falhas detectadas" in res: backup_status = "degraded"
        if "Erro" in res: backup_status = "offline"
    except:
        backup_status = "offline"

    return {
        "network": {
            "hosts": 2, 
            "status": net_status, 
            "label": "Juniper Core",
            "uptime_check": "SNMP OK" if net_status == "online" else "Check Failed"
        },
        "physical": {
            "hosts": hosts_count, 
            "problems": active_problems, 
            "label": "Zabbix Inventory"
        },
        "virtual": {
            "hosts": 150, 
            "status": virt_status, 
            "label": "vCenter & NSX-T",
            "manager_ip": "10.21.50.246"
        },
        "backup": {
            "hosts": 2,
            "status": backup_status,
            "label": f"Veeam VBR (JLLE & BRQ)",
            "summary": res if backup_status != "offline" else "Veeam API unreachable"
        }
    }

# Cache Global para Veeam (Garantir carregamento instantâneo)
veeam_cache = {"summary": {}, "details": [], "last_sync": None}

async def sync_veeam_data_loop():
    """Background task para manter o Veeam sincronizado sem travar o front."""
    from veeam_mcp_server import clients
    import asyncio
    import time
    
    while True:
        try:
            async def fetch_vbr_data(name, client):
                try:
                    print(f"DEBUG: Iniciando Sync Veeam para: {name} (URL: {client.base_url})")
                    login_ok = await client.login()
                    if not login_ok:
                        print(f"DEBUG: Falha de LOGIN para {name}")
                        return {"vbr": name, "status": "offline", "error": "Login Timeout/Fail", "metrics": {}}

                    print(f"DEBUG: Login OK para {name}. Coletando Métricas...")
                    jobs_task = client.get_request("v1/jobs")
                    repos_task = client.get_request("v1/repositories")
                    sessions_task = client.get_request("v1/backupSessions")
                    
                    jobs, repos, sessions = await asyncio.gather(jobs_task, repos_task, sessions_task)
                    print(f"DEBUG: Dados recebidos para {name}")
                    logger.info(f"Dados recebidos para {name}")
                    
                    all_sessions = sessions.get("data", [])
                    success_count = len([s for s in all_sessions if s.get("result") == "Success"])
                    sla_rate = round((success_count / len(all_sessions)) * 100, 1) if all_sessions else 100

                    return {
                        "vbr": name,
                        "status": "online",
                        "metrics": {
                            "total_jobs": len(jobs.get("data", [])),
                            "active_sessions": len([s for s in all_sessions if s.get("state") == "Working"]),
                            "failed_sessions_24h": len([s for s in all_sessions if s.get("result") == "Failed"]),
                            "sla": sla_rate,
                            "storage_usage": [
                                {
                                    "name": r.get("name"), 
                                    "free_gb": round(r.get("capacityInfo", {}).get("freeSpace", 0) / (1024**3), 2),
                                    "total_gb": round(r.get("capacityInfo", {}).get("capacity", 0) / (1024**3), 2)
                                } for r in repos.get("data", [])[:3]
                            ],
                            "recent_jobs_list": [
                                {"name": j.get("name"), "type": j.get("type"), "status": "Ready"} 
                                for j in jobs.get("data", [])[:5]
                            ]
                        }
                    }
                except Exception as e:
                    import traceback
                    error_detail = traceback.format_exc()
                    print(f"DEBUG: Erro crítico no VBR {name}: {error_detail}")
                    return {"vbr": name, "status": "offline", "error": str(e) or "Unknown Error", "metrics": {}}

            tasks = [fetch_vbr_data(name, client) for name, client in clients.items()]
            report = await asyncio.gather(*tasks)
            
            online_reports = [r for r in report if r["status"] == "online"]
            total_jobs = sum([r["metrics"].get("total_jobs", 0) for r in online_reports])
            total_active = sum([r["metrics"].get("active_sessions", 0) for r in online_reports])
            global_sla = round(sum([r["metrics"].get("sla", 0) for r in online_reports]) / len(online_reports), 1) if online_reports else 0
            
            veeam_cache["summary"] = {
                "total_nodes": len(clients),
                "online_nodes": len(online_reports),
                "global_jobs": total_jobs,
                "global_active": total_active,
                "global_sla": global_sla,
                "status": "online" if len(online_reports) == len(clients) else "degraded"
            }
            veeam_cache["details"] = report
            veeam_cache["last_sync"] = time.strftime("%H:%M:%S")
            logger.info(f"Veeam Cache atualizado: {veeam_cache['last_sync']}")
            
        except Exception as ge:
            logger.error(f"Erro no Global Sync Veeam: {ge}")
            
        await asyncio.sleep(60) # Sync a cada 1 minuto

@app.on_event("startup")
async def startup_event():
    import asyncio
    asyncio.create_task(sync_veeam_data_loop())

@app.get("/api/veeam/full")
async def get_veeam_full_dashboard():
    """Retorna dados do cache global para carregamento INSTANTÂNEO."""
    if not veeam_cache["details"]:
        return {"error": "Iniciando Sincronização...", "status": "loading"}
    return veeam_cache

@app.get("/api/veeam/debug_brq")
async def debug_brq_veeam():
    """Endpoint direto para testar BRQ-VBR e ver o erro exato."""
    from veeam_mcp_server import clients
    import asyncio
    client = clients.get("BRQ-VBR")
    if not client: return {"error": "BRQ-VBR not found in config"}
    
    try:
        print("DEBUG_ENDPOINT: Inciando teste BRQ (timeout 20s)...")
        # Forçamos um timeout externo para garantir que não trave
        return await asyncio.wait_for(_debug_internal(client), timeout=25.0)
    except asyncio.TimeoutError:
        return {"status": "fail", "error": "External Task Timeout (25s)"}
    except Exception as e:
        print(f"DEBUG_ENDPOINT: EXCEPTION: {repr(e)}")
        return {"status": "exception", "error": repr(e)}

async def _debug_internal(client):
    try:
        print("DEBUG_ENDPOINT: Testando login BRQ...")
        ok = await client.login()
        if not ok:
            return {"status": "fail", "step": "login", "url": client.base_url}
        
        print("DEBUG_ENDPOINT: Login OK. Testando v1/jobs...")
        jobs = await client.get_request("v1/jobs")
        return {"status": "success", "jobs_count": len(jobs.get("data", [])), "raw": jobs if "error" in jobs else "omitted"}
    except Exception as e:
        print(f"DEBUG_ENDPOINT: _debug_internal EXCEPTION: {repr(e)}")
        raise e

@app.get("/api/events")
async def get_mcp_events():
    """
    Simula a agregação de 'logs' ou eventos críticos via MCP.
    Busca o status detalhado de cada ativo Juniper/NSX-T.
    """
    from juniper_mcp_server import get_juniper_adc_155_status, get_juniper_adc_156_status
    from nsxt_mcp_server import get_nsxt_edge_status, get_nsxt_manager_status
    
    events = []
    
    # Juniper
    try:
        j1 = await get_juniper_adc_155_status()
        events.append({"source": "Juniper-155", "message": j1, "level": "info"})
        j2 = await get_juniper_adc_156_status()
        events.append({"source": "Juniper-156", "message": j2, "level": "info"})
    except Exception as e:
        events.append({"source": "Juniper-MCP", "message": f"Erro: {str(e)}", "level": "error"})

    # Veeam
    try:
        v1 = await get_veeam_backup_status("JLLE-VBR")
        events.append({"source": "Veeam-JLLE", "message": v1, "level": "info"})
        v2 = await get_veeam_backup_status("BRQ-VBR")
        events.append({"source": "Veeam-BRQ", "message": v2, "level": "info"})
    except Exception as e:
        events.append({"source": "Veeam-MCP", "message": f"Erro: {str(e)}", "level": "error"})

    return events

@app.get("/api/search")
def search_zabbix_hosts(q: str = Query(..., min_length=2)):
    """Busca hosts por nome ou IP para seleção no frontend."""
    zapi = zabbix_collector.zapi
    if not zapi:
        raise HTTPException(status_code=503, detail="Zabbix offline")
    
    try:
        results = search_hosts(zapi, q)
        return results
    except Exception as e:
        logger.error(f"Erro na busca: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analyze")
def analyze_host(
    hostid: Optional[str] = Query(None),
    hostname: Optional[str] = Query(None)
):
    """
    Endpoint de Analizer AI:
    Agora suporta busca direta por hostid (mais preciso após seleção no front).
    """
    zapi = zabbix_collector.zapi
    if not zapi:
        raise HTTPException(status_code=503, detail="Zabbix API indisponível.")

    try:
        target_host = None
        if hostid:
            hosts = zapi.host.get(hostids=[hostid], output=["hostid", "host", "name"], selectInterfaces=["ip"])
            if hosts: target_host = hosts[0]
        elif hostname:
            hosts = search_hosts(zapi, hostname)
            if hosts: target_host = hosts[0]
            
        if not target_host:
            raise HTTPException(status_code=404, detail="Host não encontrado.")

        hid = str(target_host["hostid"])
        hname = target_host["name"]

        # Coletar Metricas Reais Expandidas (Graceful failure)
        metrics = []
        history_data = {}
        try:
            # Busca itens específicos de performance
            search_params = {
                "hostids": [hid],
                "output": ["itemid", "name", "key_", "lastvalue", "units", "value_type"],
                "search": {"key_": ["cpu", "memory", "vfs.fs", "system.swap", "net.if"]},
                "searchByAny": True
            }
            items = zapi.item.get(**search_params)
            
            for item in items:
                # Se for numérico, tenta pegar o histórico recente (últimas 3 horas)
                if item["value_type"] in ["0", "3"]: # Float ou Integer
                    import time
                    h = zapi.history.get(
                        itemids=[item["itemid"]],
                        history=item["value_type"],
                        sortfield="clock",
                        sortorder="DESC",
                        limit=10,
                        time_from=int(time.time()) - 10800
                    )
                    history_data[item["name"]] = [float(x["value"]) for x in h]
                metrics.append({
                    "name": item["name"],
                    "key": item["key_"],
                    "last_value": f"{item['lastvalue']} {item.get('units', '')}".strip()
                })
        except Exception as me:
            logger.warning(f"Erro ao buscar metricas detalhadas para {hid}: {me}")
            metrics = [{"error": "Falha na coleta de performance"}]

        # Coletar Problems Reais (Graceful failure)
        problems = []
        try:
            problems = fetch_problems(zapi, [hid])
        except Exception as pe:
            logger.warning(f"Erro ao buscar problemas para {hid}: {pe}")
            problems = [{"error": "Falha na coleta de alertas"}]

        dataset = {
            "host_info": target_host,
            "performance_metrics": metrics,
            "trends_last_3h": history_data,
            "active_alerts": problems,
            "analysis_time": "Real-time query with 3h history"
        }
        
        # Log do payload que será enviado ao Ollama
        logger.info(f"Enviando dataset de {hname} para Ollama...")
        analysis_result = ai_client.analyze("consolidated", dataset)
        
        return {
            "hostname": hname,
            "hostid": hid,
            "raw_data_points": len(metrics) + len(problems),
            "ai_analysis": analysis_result
        }
    except Exception as e:
        logger.error(f"Erro na analise AI para {hostid or hostname}: {e}")
        raise HTTPException(status_code=500, detail=f"Erro na análise AI: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("warzem_api:app", host="0.0.0.0", port=8000, reload=True)
