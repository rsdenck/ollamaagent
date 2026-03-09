import logging
from typing import List, Dict
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    before_sleep=lambda retry_state: logger.warning(
        "Zabbix fetch_problems falhou: %s. Tentando novamente...", 
        retry_state.outcome.exception()
    )
)
def fetch_problems(zapi, hostids: List[str] = None) -> List[Dict]:
    # Fetch problems (read-only). We rely on the public endpoint; adjust fields as needed.
    params = {
        "output": ["eventid", "name", "clock", "acknowledged", "severity"],
        "sortfield": "clock",
        "sortorder": "DESC",
    }
    if hostids:
        params["hostids"] = hostids
    return zapi.problem.get(**params)
