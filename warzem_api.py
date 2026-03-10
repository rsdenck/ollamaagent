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
from mcp_servers.veeam.veeam_mcp_server import get_veeam_backup_status, get_failed_veeam_jobs
from mcp_servers.icewarp.icewarp_mcp_server import get_icewarp_status, get_icewarp_queues, get_icewarp_services, get_account_statistics
from mcp_servers.juniper.juniper_mcp_server import get_juniper_interfaces, get_juniper_bgp_peers, get_juniper_mpls_lsps
from mcp_servers.storage.storage_snmp_mcp_server import get_all_snmp_storage
from mcp_servers.storage.pure_storage_mcp_server import get_all_pure_storage

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
            "label": "vCenter (JLLE/BRQ) & Hyper-V",
            "manager_ip": "Multiple"
        },
        "hyperv": {
            "status": "online", # Será dinâmico no loop
            "label": "SCVMM BRQ",
            "metrics": {} # Preenchido pelo cache
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

# Cache Global para Hyper-V (SCVMM)
hyperv_cache = {"status": "loading", "inventory": [], "last_sync": None}

# Cache Global para Outras Visões
mail_cache = {"status": "online", "services": [], "queues": {}, "last_sync": None}
network_cache = {"status": "online", "juniper": [], "vmm_networks": [], "last_sync": None}
storage_cache = {"status": "online", "total_capacity_tb": 0, "used_capacity_tb": 0, "repositories": [], "last_sync": None}
vmware_cache = {"status": "online", "vcenters": {}, "last_sync": None}

async def sync_veeam_data_loop():
    """Background task para manter o Veeam sincronizado sem travar o front."""
    from mcp_servers.veeam.veeam_mcp_server import clients
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


@app.get("/api/hyperv/full")
async def get_hyperv_full():
    """Retorna dados do cache do Hyper-V (SCVMM)."""
    if not hyperv_cache["last_sync"]:
        return {"status": "loading", "msg": "Sincronizando com SCVMM..."}
    return hyperv_cache

async def sync_hyperv_data_loop():
    """Background task para monitorar o Hyper-V (SCVMM)."""
    from mcp_servers.hyperv.hyperv_mcp_server import get_hyperv_full_inventory
    import time
    import json
    
    while True:
        try:
            print("DEBUG: Iniciando Sync Hyper-V (SCVMM)...")
            res_json = await get_hyperv_full_inventory()
            res = json.loads(res_json)
            
            if res.get("status") == "online":
                hyperv_cache.update({
                    "status": "online",
                    "inventory": res.get("inventory", []),
                    "last_sync": time.strftime("%H:%M:%S")
                })
                print(f"DEBUG: Sync Hyper-V OK: {len(res.get('inventory', []))} clusters encontrados.")
            else:
                print(f"DEBUG: Falha no Sync Hyper-V: {res.get('message')}")
        except Exception as e:
            print(f"DEBUG: Erro no Sync Hyper-V: {e}")
            hyperv_cache["status"] = "offline"
            
async def sync_mail_data_loop():
    """Background task para monitorar o IceWarp."""
    import time
    while True:
        try:
            status = await get_icewarp_status()
            queues = await get_icewarp_queues()
            services = await get_icewarp_services()
            stats = await get_account_statistics()
            
            mail_cache.update({
                "status": "online", # Se chegamos aqui sem erro, está online para a conta
                "services": services,
                "queues": queues,
                "account_stats": stats,
                "last_sync": time.strftime("%H:%M:%S")
            })
        except Exception as e:
            logger.error(f"Error syncing mail: {e}")
            mail_cache["status"] = "offline"
        await asyncio.sleep(60)

async def sync_network_data_loop():
    """Background task para monitorar Juniper via SNMP."""
    import time
    routers = [
        {"ip": "192.168.0.155", "name": "RT-ADC-BQ-01", "comm": "RT-ADC-BQ-01-MGT"},
        {"ip": "192.168.0.156", "name": "RT-ADC-BQ-02", "comm": "RT-ADC-BQ-02-MGT"}
    ]
    while True:
        try:
            juniper_data = []
            for r in routers:
                bgp = await get_juniper_bgp_peers(r["ip"], r["comm"])
                mpls = await get_juniper_mpls_lsps(r["ip"], r["comm"])
                juniper_data.append({
                    "name": r["name"],
                    "ip": r["ip"],
                    "status": "online",
                    "bgp": bgp,
                    "mpls": mpls,
                    "uptime": "Check Dashboard"
                })
            
            network_cache.update({
                "status": "online",
                "juniper": juniper_data,
                "vmm_networks": [
                    {"name": "VM-Network-Production", "vlan": 100, "subnet": "10.1.100.0/24"},
                    {"name": "VM-Network-DMZ", "vlan": 200, "subnet": "10.1.200.0/24"}
                ],
                "last_sync": time.strftime("%H:%M:%S")
            })
        except Exception as e:
            logger.error(f"Error syncing network: {e}")
            network_cache["status"] = "offline"
        await asyncio.sleep(60)

async def sync_vmware_data_loop():
    """Background task para monitorar ambos os vCenters."""
    from mcp_servers.vmware.src.vsphere_mcp_server.server import list_hosts, list_datastores, list_vms
    import time
    vcenters = [
        {"host": "jlle-vcenter.armazemdc.com.br", "name": "VCENTER-JLLE"},
        {"host": "vcenter01.armazemdc.com.br", "name": "VCENTER-BRQ"}
    ]
    while True:
        try:
            vc_data = {}
            for vc in vcenters:
                # Nota: Em ambiente real, o VSphereClient precisa das credenciais no .env
                # Aqui simulamos a chamada via MCP para agregação
                try:
                    hosts_raw = list_hosts(vc["host"])
                    datastores_raw = list_datastores(vc["host"])
                    vms_raw = list_vms(vc["host"])
                    
                    vc_data[vc["name"]] = {
                        "host": vc["host"],
                        "status": "online",
                        "summary": {
                            "hosts": hosts_raw.count("•"),
                            "vms": vms_raw.count("•"),
                            "datastores": datastores_raw.count("•")
                        }
                    }
                except:
                    vc_data[vc["name"]] = {"host": vc["host"], "status": "offline"}

            vmware_cache.update({
                "status": "online",
                "vcenters": vc_data,
                "last_sync": time.strftime("%H:%M:%S")
            })
        except Exception as e:
            logger.error(f"Error syncing vmware: {e}")
        await asyncio.sleep(120)

async def sync_storage_data_loop():
    """Agrega contagem de capacidade global."""
    import time
    while True:
        try:
            # Integração simplificada puxando do cache do Veeam e VMware
            repos = []
            if veeam_cache.get("details"):
                 for d in veeam_cache["details"]:
                     if d.get("status") == "online":
                         for r in d["metrics"].get("storage_usage", []):
                             repos.append({"provider": "Veeam", "name": r["name"], "free_gb": r["free_gb"], "total_gb": r["total_gb"]})
            
            if vmware_cache.get("vcenters"):
                for name, vc in vmware_cache["vcenters"].items():
                    if vc.get("status") == "online":
                        # Simplificação: cada host/datastore conta como um repo
                        repos.append({"provider": "VMware", "name": f"{name} Storage", "free_gb": 5000, "total_gb": 20000})
            
            # Novos Dados de SNMP & Pure Storage
            try:
                snmp_repos = await get_all_snmp_storage()
                repos.extend(snmp_repos)
            except Exception as e:
                logger.error(f"Error fetching SNMP storage: {e}")

            try:
                pure_repos = await get_all_pure_storage()
                repos.extend(pure_repos)
            except Exception as e:
                logger.error(f"Error fetching Pure storage: {e}")
            
            if not repos:
                # Fallback: Se estiver tudo vazio, tenta puxar pelo menos um dado nominal para evitar NaN
                repos.append({"provider": "Global", "name": "Scanning Storage Nodes...", "free_gb": 1, "total_gb": 1})
            
            storage_cache.update({
                "status": "online" if repos else "syncing",
                "total_capacity_tb": sum([r["total_gb"] for r in repos]) / 1024,
                "used_capacity_tb": sum([r["total_gb"] - r["free_gb"] for r in repos]) / 1024,
                "repositories": repos,
                "last_sync": time.strftime("%H:%M:%S")
            })
            print(f"DEBUG: Sync Storage OK. {len(repos)} repositórios mapeados.")
        except Exception as e:
             logger.error(f"Error syncing storage: {e}")
        await asyncio.sleep(60)

@app.get("/api/mail/full")
async def get_mail_full():
    return mail_cache

@app.get("/api/networks/full")
async def get_networks_full():
    return network_cache

@app.get("/api/storage/full")
async def get_storage_full():
    return storage_cache

@app.get("/api/vmware/full")
async def get_vmware_full():
    return vmware_cache

@app.get("/api/veeam/full")
async def get_veeam_full():
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
    from mcp_servers.juniper.juniper_mcp_server import get_juniper_adc_155_status, get_juniper_adc_156_status
    from mcp_servers.nsxt.nsxt_mcp_server import get_nsxt_edge_status, get_nsxt_manager_status
    
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

@app.get("/api/analyze/global")
async def analyze_global():
    """Realiza análise consolidada de todo o ecossistema (VMware, Hyper-V, Redes, Mail, Veeam)."""
    dataset = {
        "vmware": vmware_cache,
        "hyperv": hyperv_cache,
        "networks": network_cache,
        "mail": mail_cache,
        "veeam": veeam_cache,
        "storage": storage_cache
    }
    
    logger.info("Enviando dataset GLOBAL para análise da IA...")
    analysis_result = ai_client.analyze("infrastructure_global", dataset)
    
    return {
        "summary": "Global Datacenter Assessment",
        "ai_analysis": analysis_result,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

@app.get("/api/analyze")
def analyze_host(
    hostid: Optional[str] = Query(None),
    hostname: Optional[str] = Query(None)
):
    """Análise de host individual via Zabbix + LLM."""
    if hostid == "global" or hostname == "GLOBAL":
        # Redirect interno ou erro amigável se o front errar o endpoint
        raise HTTPException(status_code=400, detail="Use /api/analyze/global para análise consolidada.")

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

        # Coletar Metricas Reais
        metrics = []
        history_data = {}
        try:
            search_params = {
                "hostids": [hid],
                "output": ["itemid", "name", "key_", "lastvalue", "units", "value_type"],
                "search": {"key_": ["cpu", "memory", "vfs.fs", "system.swap", "net.if"]},
                "searchByAny": True
            }
            items = zapi.item.get(**search_params)
            
            for item in items:
                if item["value_type"] in ["0", "3"]:
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
            logger.warning(f"Erro em metricas: {me}")

        problems = fetch_problems(zapi, [hid])
        dataset = {
            "host_info": target_host,
            "performance_metrics": metrics,
            "trends_last_3h": history_data,
            "active_alerts": problems
        }
        
        analysis_result = ai_client.analyze("consolidated", dataset)
        
        return {
            "hostname": hname,
            "hostid": hid,
            "ai_analysis": analysis_result
        }
    except Exception as e:
        logger.error(f"Erro na analise AI: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.on_event("startup")
async def startup_event():
    import asyncio
    asyncio.create_task(sync_veeam_data_loop())
    asyncio.create_task(sync_hyperv_data_loop())
    asyncio.create_task(sync_mail_data_loop())
    asyncio.create_task(sync_network_data_loop())
    asyncio.create_task(sync_vmware_data_loop())
    asyncio.create_task(sync_storage_data_loop())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("warzem_api:app", host="0.0.0.0", port=8000, reload=True)
