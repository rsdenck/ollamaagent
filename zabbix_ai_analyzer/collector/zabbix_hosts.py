import logging
from typing import List, Dict
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    before_sleep=lambda retry_state: logger.warning(
        "Zabbix fetch_hosts falhou: %s. Tentando novamente...", 
        retry_state.outcome.exception()
    )
)
def fetch_hosts(zapi) -> List[Dict]:
    """Fetch Zabbix hosts (read-only).
    Returns a list of host dicts with basic fields.
    """
    return zapi.host.get(output=["hostid", "host", "name", "status", "available"])

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    before_sleep=lambda retry_state: logger.warning(
        "Zabbix search_hosts falhou: %s. Tentando novamente...", 
        retry_state.outcome.exception()
    )
)
def search_hosts(zapi, query: str) -> List[Dict]:
    """
    Busca hosts no Zabbix por:
    - Technical Name (host)
    - Visible Name (name)
    - IP Address (interface.ip)
    """
    # 1. Busca por Nome/Visible Name
    hosts_by_name = zapi.host.get(
        output=["hostid", "host", "name", "status", "available"],
        selectInterfaces=["ip"],
        search={
            "host": query,
            "name": query
        },
        searchByAny=True,
        limit=10
    )
    
    # 2. Busca por IP (via interfaces)
    interfaces = zapi.hostinterface.get(
        output=["hostid", "ip"],
        search={"ip": query},
        limit=10
    )
    
    host_ids_by_ip = [i["hostid"] for i in interfaces]
    
    hosts_by_ip = []
    if host_ids_by_ip:
        hosts_by_ip = zapi.host.get(
            output=["hostid", "host", "name", "status", "available"],
            selectInterfaces=["ip"],
            hostids=host_ids_by_ip
        )
    
    # Combinar e remover duplicatas por hostid
    combined = {h["hostid"]: h for h in (hosts_by_name + hosts_by_ip)}
    
    # Formatar para o frontend (incluindo IP principal no objeto host)
    results = []
    for h in combined.values():
        ip = h.get("interfaces", [{}])[0].get("ip", "N/A")
        h["ip"] = ip
        results.append(h)
        
    return results
