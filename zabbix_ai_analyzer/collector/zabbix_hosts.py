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
