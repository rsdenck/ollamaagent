import asyncio
import httpx
import logging

logger = logging.getLogger(__name__)

PURE_ARRAYS = [
    "10.21.0.30",
    "10.21.0.15",
    "10.21.0.10",
    "10.21.0.5",
    "10.21.0.8",
    "192.168.128.130"
]

# Note: API Token would normally be in .env
API_TOKEN = "MOCK_TOKEN" 

async def get_pure_storage_metrics(ip):
    """Fetches metrics from a Pure Storage array via REST API."""
    url = f"https://{ip}/api/2.x/arrays/space"
    # Note: In a real scenario, we'd need a valid API token for authentication
    headers = {
        "x-auth-token": API_TOKEN,
        "Content-Type": "application/json"
    }
    
    try:
        # Mocking the response for now as we don't have real credentials
        # In a real environment, we'd use:
        # async with httpx.AsyncClient(verify=False) as client:
        #     resp = await client.get(url, headers=headers)
        #     data = resp.json()
        
        # Simulate realistic Pure Storage space data
        await asyncio.sleep(0.1)
        return {
            "name": f"Pure-{ip.split('.')[-1]}",
            "capacity": 50 * 1024**4, # 50TB
            "provisioned": 30 * 1024**4, # 30TB
            "physical": 10 * 1024**4, # 10TB
            "status": "online"
        }
    except Exception as e:
        logger.error(f"Failed to fetch Pure metrics for {ip}: {e}")
        return None

async def get_all_pure_storage():
    """Aggregates metrics from all configured Pure Storage arrays."""
    tasks = [get_pure_storage_metrics(ip) for ip in PURE_ARRAYS]
    results = await asyncio.gather(*tasks)
    
    all_repos = []
    for i, res in enumerate(results):
        if res:
            ip = PURE_ARRAYS[i]
            total_gb = res["capacity"] / (1024**3)
            used_gb = res["physical"] / (1024**3) # Simplified for now
            all_repos.append({
                "provider": "PureStorage",
                "host": ip,
                "name": f"Pure Array {ip}",
                "total_gb": round(total_gb, 2),
                "used_gb": round(used_gb, 2),
                "free_gb": round(total_gb - used_gb, 2),
                "status": res["status"]
            })
    return all_repos
