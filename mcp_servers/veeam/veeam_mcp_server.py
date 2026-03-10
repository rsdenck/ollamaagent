import os
import asyncio
import httpx
import logging
from typing import Dict, Any, List
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP Server for Veeam
mcp = FastMCP("veeam-mcp-server")
logger = logging.getLogger("veeam.mcp")

class VeeamClient:
    def __init__(self, host: str, user: str, password: str, port: int = 9419):
        self.base_url = f"https://{host}:{port}/api"
        self.user = user
        self.password = password
        self.client_kwargs = {
            "verify": False,
            "timeout": httpx.Timeout(30.0, connect=10.0),
            "headers": {"Accept": "application/json"}
        }

    async def login(self):
        try:
            url = f"{self.base_url}/oauth2/token"
            payload = {
                "grant_type": "password",
                "username": self.user,
                "password": self.password
            }
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded"
            }
            async with httpx.AsyncClient(**self.client_kwargs) as client:
                print(f"DEBUG: Tentando login em {url}...")
                response = await client.post(url, data=payload, headers=headers)
                
                if response.status_code == 200:
                    self.token = response.json().get("access_token")
                    print(f"DEBUG: Login Success para {self.base_url}")
                    return True
                
                print(f"DEBUG: Login Failed para {self.base_url}: {response.status_code}")
                return False
        except Exception as e:
            print(f"DEBUG: Login Exception para {self.base_url}: {repr(e)}")
            return False

    async def get_request(self, endpoint: str):
        if not self.token:
            await self.login()
        
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json"
        }
        async with httpx.AsyncClient(**self.client_kwargs) as client:
            response = await client.get(f"{self.base_url}/{endpoint}", headers=headers)
        if response.status_code == 401: # Token expired
            await self.login()
            headers["Authorization"] = f"Bearer {self.token}"
            async with httpx.AsyncClient(**self.client_kwargs) as client:
                response = await client.get(f"{self.base_url}/{endpoint}", headers=headers)
        
        return response.json() if response.status_code == 200 else {"error": response.status_code, "msg": response.text}

# VBR Configs
VBRS = {
    "JLLE-VBR": {"host": "10.21.40.5", "user": "zabbix_hyv", "pass": "a!7d#fbp!@#!@#"},
    "BRQ-VBR": {"host": "10.1.247.5", "user": "zabbix_hyv", "pass": "a!7d#fbp!@#!@#"}
}

clients = {name: VeeamClient(cfg["host"], cfg["user"], cfg["pass"]) for name, cfg in VBRS.items()}

@mcp.tool()
async def get_veeam_backup_status(vbr_name: str) -> str:
    """
    Retorna o status geral de backup de um servidor VBR especifico (JLLE-VBR ou BRQ-VBR).
    Lista jobs, sessões recentes e status de repositórios.
    """
    client = clients.get(vbr_name)
    if not client:
        return f"VBR {vbr_name} não configurado."

    try:
        # Jobs summary
        jobs = await client.get_request("v1/jobs")
        # Sessions summary (recent backups)
        sessions = await client.get_request("v1/backupSessions")
        # Repositories (Capacity)
        repos = await client.get_request("v1/repositories")

        summary = f"--- STATUS VEEAM: {vbr_name} ---\n"
        
        if isinstance(jobs, dict) and "data" in jobs:
            summary += f"Jobs Totais: {len(jobs['data'])}\n"
        
        if isinstance(repos, dict) and "data" in repos:
            summary += "Repositórios:\n"
            for r in repos['data'][:3]:
                name = r.get('name')
                # Simplificação do dado de capacidade (Veeam V12 path)
                capacity = r.get('capacityInfo', {})
                summary += f" - {name}: Total={capacity.get('capacity', 0)}B, Free={capacity.get('freeSpace', 0)}B\n"
        
        return summary
    except Exception as e:
        return f"Erro ao coletar dados do {vbr_name}: {str(e)}"

@mcp.tool()
async def get_failed_veeam_jobs() -> str:
    """Busca sessões com falha em todos os servidores VBR configurados."""
    results = []
    for name, client in clients.items():
        try:
            # Filtro simplificado manual nos resultados ou via query param se suportado
            sessions = await client.get_request("v1/backupSessions")
            if isinstance(sessions, dict) and "data" in sessions:
                failed = [s for s in sessions['data'] if s.get('result') == 'Failed']
                if failed:
                    results.append(f"{name}: {len(failed)} falhas detectadas nas sessões recentes.")
                else:
                    results.append(f"{name}: Tudo OK (Nenhuma falha recente).")
        except:
            results.append(f"{name}: Erro de conexão.")
    
    return "\n".join(results)

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    mcp.run()
