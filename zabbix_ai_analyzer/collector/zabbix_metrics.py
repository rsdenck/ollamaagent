import logging
from typing import List, Dict
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    before_sleep=lambda retry_state: logger.warning(
        "Zabbix fetch_metrics falhou: %s. Tentando novamente...", 
        retry_state.outcome.exception()
    )
)
def fetch_metrics(zapi, hostids: List[str]) -> List[Dict]:
    if not hostids:
        return []
    # Fetch items for the hosts with last value
    return zapi.item.get(
        hostids=hostids, output=["itemid", "name", "key_", "lastvalue", "hostid"]
    )
