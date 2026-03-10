import asyncio
import httpx
import urllib3
from veeam_mcp_server import VeeamClient

async def debug():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    name = "BRQ-VBR"
    host = "10.1.247.5"
    user = "zabbix_hyv"
    password = "a!7d#fbp!@#!@#"
    
    print(f"Testing {name} at {host}...")
    client = VeeamClient(host, user, password)
    
    try:
        print("Attempting login...")
        ok = await client.login()
        if ok:
            print("Login Success!")
            print("Fetching jobs...")
            jobs = await client.get_request("v1/jobs")
            print(f"Jobs found: {len(jobs.get('data', []))}")
        else:
            print("Login Failed.")
    except Exception as e:
        print(f"Exception happened: {type(e).__name__}: {e}")

if __name__ == "__main__":
    asyncio.run(debug())
