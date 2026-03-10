import os
import json
import asyncio
import subprocess
import logging
from typing import Dict, Any, List
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP Server for Hyper-V
mcp = FastMCP("hyperv-mcp-server")
logger = logging.getLogger("hyperv.mcp")

# SCVMM Config
SCVMM_CONFIG = {
    "server": "scvmm01.armazemdc.com.br",
    "user": "ARMAZEMDC\\zabbix_hyv",
    "pass": "a!7d#fbp!@#!@#"
}

def run_powershell(command: str) -> Dict[str, Any]:
    """Executa um comando PowerShell e retorna o output JSON."""
    try:
        # Wrap de credenciais se necessário ou execução direta se o processo já tiver permissão
        # Para lab, assumimos execução direta ou pass-through de credenciais via shell.
        full_cmd = f"$secpasswd = ConvertTo-SecureString '{SCVMM_CONFIG['pass']}' -AsPlainText -Force; " \
                  f"$creds = New-Object System.Management.Automation.PSCredential('{SCVMM_CONFIG['user']}', $secpasswd); " \
                  f"Invoke-Command -ComputerName {SCVMM_CONFIG['server']} -Credential $creds -ScriptBlock {{ " \
                  f"Import-Module VirtualMachineManager; " \
                  f"{command} | ConvertTo-Json -Depth 4 }}"
        
        process = subprocess.run(
            ["powershell", "-Command", full_cmd],
            capture_output=True,
            text=True,
            check=True
        )
        if not process.stdout.strip():
            return {"error": "Sem retorno do PowerShell"}
        return json.loads(process.stdout)
    except subprocess.CalledProcessError as e:
        logger.error(f"Erro PS: {e.stderr}")
        return {"error": str(e), "details": e.stderr}
    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}")
        return {"error": str(e)}

@mcp.tool()
async def get_hyperv_full_inventory() -> str:
    """
    Retorna o inventário completo do SCVMM: Clusters -> Hosts -> VMs.
    """
    cmd = """
    $inventory = @()
    $clusters = Get-SCVMHostCluster
    foreach ($cluster in $clusters) {
        $clusterObj = @{
            Name = $cluster.Name
            TotalMemory = $cluster.TotalMemory
            CPUUtilization = $cluster.CPUUtilization
            Hosts = @()
        }
        $hosts = Get-SCVMHost -VMHostCluster $cluster
        foreach ($host in $hosts) {
            $hostObj = @{
                Name = $host.Name
                State = $host.OverallState.ToString()
                TotalMemory = $host.TotalMemory
                AvailableMemory = $host.AvailableMemory
                CPUUtilization = $host.CPUUtilization
                VMs = @()
            }
            $vms = Get-SCVirtualMachine -VMHost $host
            foreach ($vm in $vms) {
                $hostObj.VMs += @{
                    Name = $vm.Name
                    Status = $vm.Status.ToString()
                    CPUUsage = $vm.CPUUsage
                    Memory = $vm.Memory
                    IP = $vm.IPv4Addresses[0]
                }
            }
            $clusterObj.Hosts += $hostObj
        }
        $inventory += $clusterObj
    }
    $inventory
    """
    data = run_powershell(cmd.strip())
    
    if "error" in data:
        return json.dumps({"status": "error", "message": data['error']})
    
    return json.dumps({
        "status": "online",
        "last_sync": "Agora",
        "inventory": data if isinstance(data, list) else [data]
    })

if __name__ == "__main__":
    mcp.run()
