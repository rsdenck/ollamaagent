import os
from dotenv import load_dotenv
from pyzabbix import ZabbixAPI
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

ZABBIX_URL = os.getenv("ZABBIX_URL")
ZABBIX_USER = os.getenv("ZABBIX_USER")
ZABBIX_PASS = os.getenv("ZABBIX_PASS")

def test_search(query):
    zapi = ZabbixAPI(ZABBIX_URL)
    zapi.login(ZABBIX_USER, ZABBIX_PASS)
    logger.info("Zabbix Login OK")
    
    # 1. Search by name/visible name
    hosts_by_name = zapi.host.get(
        output=["hostid", "host", "name"],
        search={
            "host": query,
            "name": query
        },
        searchByAny=True,
        limit=10,
        selectInterfaces=["ip"]
    )
    logger.info(f"Hosts by name/visible name: {hosts_by_name}")
    
    # 2. Search by IP
    interfaces = zapi.hostinterface.get(
        output=["hostid", "ip"],
        search={"ip": query},
        limit=10
    )
    logger.info(f"Interfaces for IP search: {interfaces}")
    
    host_ids_by_ip = [i["hostid"] for i in interfaces]
    if host_ids_by_ip:
        hosts_by_ip = zapi.host.get(
            output=["hostid", "host", "name"],
            hostids=host_ids_by_ip,
            selectInterfaces=["ip"]
        )
        logger.info(f"Hosts by IP search: {hosts_by_ip}")
    else:
        logger.info("No host IDs found for IP search.")

if __name__ == "__main__":
    import sys
    q = sys.argv[1] if len(sys.argv) > 1 else "192.168.128.220"
    test_search(q)
