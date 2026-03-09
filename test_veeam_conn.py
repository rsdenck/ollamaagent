import asyncio
import httpx
import json

async def test_veeam():
    host = "10.1.247.5"
    port = 9419
    user = "zabbix_hyv"
    password = "a!7d#fbp!@#!@#"
    
    base_url = f"https://{host}:{port}/api"
    print(f"Testing login at {base_url}/oauth2/token")
    
    async with httpx.AsyncClient(verify=False) as client:
        try:
            url = f"{base_url}/oauth2/token"
            data = {
                "grant_type": "password",
                "username": user,
                "password": password
            }
            headers = {"Accept": "application/json"}
            
            print("Sending POST request...")
            response = await client.post(url, data=data, headers=headers, timeout=15)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 200:
                token = response.json().get("access_token")
                print("Login Success!")
                
                headers["Authorization"] = f"Bearer {token}"
                print("Fetching jobs...")
                res_jobs = await client.get(f"{base_url}/v1/jobs", headers=headers, timeout=15)
                print(f"Jobs Status: {res_jobs.status_code}")
                
                print("Fetching repositories...")
                res_repos = await client.get(f"{base_url}/v1/repositories", headers=headers, timeout=15)
                print(f"Repos Status: {res_repos.status_code}")
                # print(f"Repos Data: {res_repos.text}")

                print("Fetching sessions...")
                res_sessions = await client.get(f"{base_url}/v1/backupSessions", headers=headers, timeout=15)
                print(f"Sessions Status: {res_sessions.status_code}")
                
            else:
                print("Login Failed.")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    asyncio.run(test_veeam())
