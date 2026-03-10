import asyncio
import logging
from pysnmp.hlapi.asyncio import *

logger = logging.getLogger(__name__)

STORAGE_HOSTS = [
    "192.168.128.220",
    "192.168.128.221",
    "192.168.128.103",
    "192.168.128.102",
    "192.168.128.101",
    "192.168.128.120"
]

COMMUNITY = "public"

# OIDs for HOST-RESOURCES-MIB::hrStorageTable
OID_HR_STORAGE_INDEX = "1.3.6.1.2.1.25.2.3.1.1"
OID_HR_STORAGE_TYPE = "1.3.6.1.2.1.25.2.3.1.2"
OID_HR_STORAGE_DESCR = "1.3.6.1.2.1.25.2.3.1.3"
OID_HR_STORAGE_ALLOC_UNITS = "1.3.6.1.2.1.25.2.3.1.4"
OID_HR_STORAGE_SIZE = "1.3.6.1.2.1.25.2.3.1.5"
OID_HR_STORAGE_USED = "1.3.6.1.2.1.25.2.3.1.6"

async def get_snmp_storage_data(ip):
    """Fetches storage data for a specific IP using SNMP."""
    try:
        engine = SnmpEngine()
        iterator = nextCmd(
            engine,
            CommunityData(COMMUNITY),
            UdpTransportTarget((ip, 161)),
            ContextData(),
            ObjectType(ObjectIdentity(OID_HR_STORAGE_DESCR)),
            ObjectType(ObjectIdentity(OID_HR_STORAGE_ALLOC_UNITS)),
            ObjectType(ObjectIdentity(OID_HR_STORAGE_SIZE)),
            ObjectType(ObjectIdentity(OID_HR_STORAGE_USED)),
            lexicographicMode=False
        )

        storage_items = []
        async for errorIndication, errorStatus, errorIndex, varBinds in iterator:
            if errorIndication:
                logger.error(f"SNMP Error for {ip}: {errorIndication}")
                break
            elif errorStatus:
                logger.error(f"SNMP Error Status for {ip}: {errorStatus.prettyPrint()}")
                break
            else:
                descr = varBinds[0][1].prettyPrint()
                alloc_units = int(varBinds[1][1])
                size = int(varBinds[2][1])
                used = int(varBinds[3][1])

                if size > 0:
                    total_gb = (size * alloc_units) / (1024**3)
                    used_gb = (used * alloc_units) / (1024**3)
                    storage_items.append({
                        "name": descr,
                        "total_gb": round(total_gb, 2),
                        "used_gb": round(used_gb, 2),
                        "free_gb": round(total_gb - used_gb, 2)
                    })
        
        return storage_items
    except Exception as e:
        logger.error(f"Failed to fetch SNMP data for {ip}: {e}")
        return []

async def get_all_snmp_storage():
    """Aggregates storage data from all configured SNMP hosts."""
    tasks = [get_snmp_storage_data(ip) for ip in STORAGE_HOSTS]
    results = await asyncio.gather(*tasks)
    
    all_repos = []
    for i, res in enumerate(results):
        ip = STORAGE_HOSTS[i]
        for item in res:
            all_repos.append({
                "provider": "SNMP-Storage",
                "host": ip,
                "name": f"{ip} - {item['name']}",
                "total_gb": item["total_gb"],
                "used_gb": item["used_gb"],
                "free_gb": item["free_gb"]
            })
    return all_repos
