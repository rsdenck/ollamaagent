import os
import asyncio
from typing import Dict, Any, List
from mcp.server.fastmcp import FastMCP
from pysnmp.hlapi.asyncio import *

# Initialize FastMCP Server for Juniper
mcp = FastMCP("juniper-mcp-server")

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
async def get_juniper_interfaces(target_ip: str, community: str) -> str:
    """Busca tabela de interfaces (ifTable/ifXTable) do roteador Juniper."""
    # OID ifDescr (1.3.6.1.2.1.2.2.1.2) - Simplificado para retorno textual
    res = await fetch_snmp_data(target_ip, community, "1.3.6.1.2.1.2.2.1.2.1") # Exemplo Ge-0/0/0
    return f"Interface Data [{target_ip}]: {res} (Expandir para bulk no backend)"

@mcp.tool()
async def get_juniper_bgp_peers(target_ip: str, community: str) -> str:
    """Busca status dos BGP Peers no roteador Juniper."""
    # OID bgpPeerState (1.3.6.1.2.1.15.3.1.2)
    res = await fetch_snmp_data(target_ip, community, "1.3.6.1.2.1.15.3.1.2")
    return f"BGP Peer Status [{target_ip}]: {res}"

@mcp.tool()
async def get_juniper_mpls_lsps(target_ip: str, community: str) -> str:
    """Busca LSPs MPLS configurados no roteador Juniper."""
    # OID jnxMplsLspName (1.3.6.1.4.1.2636.3.2.1.1.1)
    res = await fetch_snmp_data(target_ip, community, "1.3.6.1.4.1.2636.3.2.1.1.1")
    return f"MPLS LSPS [{target_ip}]: {res}"

@mcp.tool()
async def get_juniper_adc_156_status() -> str:
    """Busca informacoes de Sistema da caixa Juniper em 192.168.0.156 (RT-ADC-BQ-02-MGT)"""
    sys_desc = await fetch_snmp_data("192.168.0.156", "RT-ADC-BQ-02-MGT", "1.3.6.1.2.1.1.1.0")
    uptime = await fetch_snmp_data("192.168.0.156", "RT-ADC-BQ-02-MGT", "1.3.6.1.2.1.1.3.0")
    return f"Juniper (192.168.0.156) -> SysDesc: {sys_desc} | Uptime: {uptime}"

@mcp.tool()
async def get_juniper_adc_155_status() -> str:
    """Busca informacoes de Sistema da caixa Juniper em 192.168.0.155 (RT-ADC-BQ-01-MGT)"""
    sys_desc = await fetch_snmp_data("192.168.0.155", "RT-ADC-BQ-01-MGT", "1.3.6.1.2.1.1.1.0")
    uptime = await fetch_snmp_data("192.168.0.155", "RT-ADC-BQ-01-MGT", "1.3.6.1.2.1.1.3.0")
    return f"Juniper (192.168.0.155) -> SysDesc: {sys_desc} | Uptime: {uptime}"

if __name__ == "__main__":
    # Exposing the server directly on STDIO (Expected by MCP standard clients)
    mcp.run()
