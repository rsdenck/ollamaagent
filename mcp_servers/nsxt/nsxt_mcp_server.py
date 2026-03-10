import os
import asyncio
from typing import Dict, Any, List
from mcp.server.fastmcp import FastMCP
from pysnmp.hlapi.asyncio import *

# Initialize FastMCP Server for NSX-T
mcp = FastMCP("nsxt-mcp-server")

async def fetch_snmp_data(target_ip: str, community: str, oid_str: str) -> str:
    """Função utilitária para puxar dado SNMP async."""
    snmp_engine = SnmpEngine()
    iterator = getCmd(
        snmp_engine,
        CommunityData(community, mpModel=1), # SNMPv2c
        UdpTransportTarget((target_ip, 161), timeout=2, retries=1),
        ContextData(),
        ObjectType(ObjectIdentity(oid_str))
    )
    
    errorIndication, errorStatus, errorIndex, varBinds = await iterator

    if errorIndication:
        return f"Erro SNMP: {errorIndication}"
    elif errorStatus:
        return f"Erro SNMP Status: {errorStatus.prettyPrint()}"
    else:
        for varBind in varBinds:
            return " = ".join([x.prettyPrint() for x in varBind])
    return "Nenhum dado retornado."

@mcp.tool()
async def get_nsxt_edge_status() -> str:
    """Busca o System Description e UpTime via SNMP do NSXEDGE01 (10.21.50.249)"""
    sys_desc = await fetch_snmp_data("10.21.50.249", "public", "1.3.6.1.2.1.1.1.0")
    uptime = await fetch_snmp_data("10.21.50.249", "public", "1.3.6.1.2.1.1.3.0")
    return f"NSXEDGE01 (10.21.50.249) -> SysDesc: {sys_desc} | Uptime: {uptime}"

@mcp.tool()
async def get_nsxt_manager_status() -> str:
    """Busca o System Description e UpTime via SNMP do NSXMANAGER01 (10.21.50.246)"""
    sys_desc = await fetch_snmp_data("10.21.50.246", "public", "1.3.6.1.2.1.1.1.0")
    uptime = await fetch_snmp_data("10.21.50.246", "public", "1.3.6.1.2.1.1.3.0")
    return f"NSXMANAGER01 (10.21.50.246) -> SysDesc: {sys_desc} | Uptime: {uptime}"

if __name__ == "__main__":
    # Exposing the server directly on STDIO (Expected by MCP standard clients)
    mcp.run()
