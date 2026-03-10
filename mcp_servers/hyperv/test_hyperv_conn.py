import subprocess
import json

SCVMM_CONFIG = {
    "server": "scvmm01.armazemdc.com.br",
    "user": "ARMAZEMDC\\zabbix_hyv",
    "pass": "a!7d#fbp!@#!@#"
}

def test_conn():
    print(f"Testing connection to {SCVMM_CONFIG['server']}...")
    # Tenta um comando simples de ping via Invoke-Command para validar credenciais
    cmd = "Get-SCVMMServer -ComputerName scvmm01.armazemdc.com.br | Select-Object Version"
    
    full_cmd = f"$secpasswd = ConvertTo-SecureString '{SCVMM_CONFIG['pass']}' -AsPlainText -Force; " \
              f"$creds = New-Object System.Management.Automation.PSCredential('{SCVMM_CONFIG['user']}', $secpasswd); " \
              f"Invoke-Command -ComputerName {SCVMM_CONFIG['server']} -Credential $creds -ScriptBlock {{ {cmd} | ConvertTo-Json }}"
    
    try:
        process = subprocess.run(
            ["powershell", "-Command", full_cmd],
            capture_output=True,
            text=True,
            check=True
        )
        print("Success! Output:")
        print(process.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    test_conn()
