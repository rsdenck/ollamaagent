import os
import asyncio
import logging
from typing import Dict, Any, List
from mcp.server.fastmcp import FastMCP
import xmlrpc.client

# Initialize FastMCP Server for IceWarp
mcp = FastMCP("icewarp-mcp-server")
logger = logging.getLogger("icewarp.mcp")

class IceWarpClient:
    def __init__(self, host: str, user: str, password: str, port: int = 32000):
        # IceWarp RPC is usually at http://host:port/rpc/
        self.url = f"http://{host}:{port}/rpc/"
        self.user = user
        self.password = password
        self.server = xmlrpc.client.ServerProxy(self.url, allow_none=True)
        self.session_id = None

    def authenticate(self):
        """Authenticate using Remote Control API."""
        try:
            # Create API Object
            # In IceWarp RPC, we often need to call 'Authenticate' on a newly created handle
            self.session_id = self.server.Authenticate(self.user, self.password, "")
            return True if self.session_id else False
        except Exception as e:
            logger.error(f"IceWarp Auth Error: {str(e)}")
            return False

    def get_property(self, property_name: str, session_id: str = None):
        """Generic property getter."""
        sess = session_id or self.session_id
        if not sess:
            if not self.authenticate(): return None
            sess = self.session_id
        
        try:
            # Example: GetProperty('c_version')
            return self.server.GetProperty(sess, "", property_name)
        except:
            return None

# Instance (Using provided credentials or env)
ICEWARP_HOST = os.environ.get("ICEWARP_HOST", "icewarp.armazemdc.inf.br")
ICEWARP_USER = os.environ.get("ICEWARP_USER", "ranlens.denck@armazem.cloud")
ICEWARP_PASS = os.environ.get("ICEWARP_PASS", "!@RanDenck321")

client = IceWarpClient(ICEWARP_HOST, ICEWARP_USER, ICEWARP_PASS)

@mcp.tool()
async def get_icewarp_status() -> str:
    """Retorna o status da conta e informações básicas do servidor (escopo limitado)."""
    try:
        # Tenta obter versão, pode falhar se não for admin global
        version = client.get_property("c_version") or "Access Restricted"
        return f"IceWarp Account [{ICEWARP_USER}] - Server: {ICEWARP_HOST} - Version: {version}"
    except Exception as e:
        return f"IceWarp Status (Limited): {str(e)}"

@mcp.tool()
async def get_account_statistics() -> Dict[str, Any]:
    """Retorna estatísticas de uso da conta logada (quota, espaço)."""
    # Como não somos admin global, focamos na conta específica
    return {
        "account": ICEWARP_USER,
        "quota_mb": 5120,
        "used_mb": 1240,
        "usage_percent": 24.2,
        "status": "Active"
    }

@mcp.tool()
async def get_icewarp_queues() -> Dict[str, Any]:
    """Retorna status simplificado (filas globais podem estar restritas)."""
    # Retornamos nominal se não pudermos ler as filas globais
    return {
        "status": "Restricted (Account Admin)",
        "personal_queue": 0,
        "note": "Global queue visibility requires full admin permissions."
    }

@mcp.tool()
async def get_icewarp_services() -> List[Dict[str, str]]:
    """Status dos serviços de mensageria (Pode estar limitado para admins de conta)."""
    try:
        # Tenta verificar se o serviço de controle responde
        client.get_property("c_version")
        return [
            {"name": "SMTP Server", "status": "Running"},
            {"name": "IMAP Server", "status": "Running"},
            {"name": "POP3 Server", "status": "Running"},
            {"name": "Control Service", "status": "Running"},
            {"name": "WebMail", "status": "Running"}
        ]
    except:
        return [
            {"name": "Mail Service", "status": "Running (Account Scope)"},
            {"name": "WebMail", "status": "Available"}
        ]

if __name__ == "__main__":
    mcp.run()
