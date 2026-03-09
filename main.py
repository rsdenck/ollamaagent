import json
import os
import sys
import logging
from typing import Dict, Any

from pyzabbix import ZabbixAPI
from dotenv import load_dotenv

from zabbix_ai_analyzer.collector.zabbix_hosts import fetch_hosts
from zabbix_ai_analyzer.collector.zabbix_metrics import fetch_metrics
from zabbix_ai_analyzer.collector.zabbix_problems import fetch_problems
from zabbix_ai_analyzer.ai.ollama_client import OllamaClient
from zabbix_ai_analyzer.core.analyzer import Analyzer

logger = logging.getLogger("zabbix_ai_analyzer.main")

class ZabbixCollector:
    """Encapsula a conexão e coleta de dados do Zabbix, abstraindo a complexidade."""
    
    def __init__(self, url: str, user: str, password: str):
        self.url = url
        self.user = user
        self.password = password
        self.zapi = self._connect()

    def _connect(self):
        """Estabelece a conexão com a API do Zabbix, permitindo graceful degradation."""
        logger.info("Iniciando conexão com Zabbix em %s", self.url)
        # Fallback de inicialização por diferentes assinaturas de versão da pyzabbix
        try:
            zapi = ZabbixAPI(server=self.url, timeout=120)
            if self.user and self.password:
                zapi.login(self.user, self.password)
            return zapi
        except TypeError:
            zapi = ZabbixAPI(server=self.url, timeout=120)
            if self.user and self.password:
                try:
                    zapi.login(self.user, self.password)
                    return zapi
                except Exception as e:
                    logger.warning("Falha na autenticação Zabbix: %s. Procedendo com acesso anônimo.", e)
            else:
                logger.warning("Credenciais Zabbix ausentes. Procedendo com acesso anônimo.")
            return zapi
        except Exception as e:
            logger.warning("Erro crítico ao conectar no Zabbix: %s. O collector não retornará dados.", e)
            return None

    def collect(self) -> Dict[str, Any]:
        """Realiza a coleta centralizada de hosts, métricas e problems."""
        if self.zapi is None:
            logger.warning("Zabbix API indisponível devido a falha de login ou conexão. Pulando coleta Zabbix.")
            return {"hosts": [], "metrics": [], "problems": []}

        try:
            logger.info("Coletando hosts do Zabbix...")
            hosts = fetch_hosts(self.zapi)
        except Exception as e:
            logger.error("Falha ao coletar hosts do Zabbix após retrys: %s", e)
            hosts = []
        
        hostids = [str(h.get("hostid")) for h in hosts if h.get("hostid") is not None][:50]
        
        metrics = []
        if hostids:
            try:
                logger.info("Coletando métricas para %d hosts...", len(hostids))
                metrics = fetch_metrics(self.zapi, hostids)
            except Exception as e:
                logger.error("Falha ao coletar métricas do Zabbix após retrys: %s", e)
        
        try:
            logger.info("Coletando problems (evetid/alerts)...")
            problems = fetch_problems(self.zapi)
        except Exception as e:
            logger.error("Falha ao coletar problems do Zabbix após retrys: %s", e)
            problems = []

        return {
            "hosts": hosts,
            "metrics": metrics,
            "problems": problems
        }

class OllamaAnalyzerApp:
    """Classe de Orquestração Principal (Application Layer)."""
    
    def __init__(self):
        self._setup_logging()
        self.zabbix_url = os.environ.get("ZABBIX_URL", "https://monitoramento.armazem.cloud/api_jsonrpc.php")
        self.zabbix_user = os.environ.get("ZABBIX_USER", "zabbix_api")
        self.zabbix_pass = os.environ.get("ZABBIX_PASS", "")
        self.ollama_address = os.environ.get("OLLAMA_ADDRESS", "http://10.1.254.32:11434")

    def _setup_logging(self):
        """Configura a observabilidade baseada na env."""
        log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
        logging.basicConfig(
            level=getattr(logging, log_level, logging.INFO),
            format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        )

    def run(self):
        """Workflow unificado de coleta e submissão aos modelos de IA."""
        try:
            # 1. Coleta os dados de forma isolada
            collector = ZabbixCollector(self.zabbix_url, self.zabbix_user, self.zabbix_pass)
            zabbix_data = collector.collect()
            
            # 2. Inicializa IA e Analyzer
            logger.info("Conectando ao Ollama em %s", self.ollama_address)
            ai_client = OllamaClient(address=self.ollama_address, model="llama3:latest", short_mode=True)
            
            analyzer = Analyzer(zabbix_data, ai_client)
            
            # 3. Executa processamento estruturado (Business Domain)
            logger.info("Executando análises IA (Health, Security, Capacity)...")
            report = {}
            for ctx in ["health", "security", "capacity"]:
                try:
                    logger.info("Analisando contexto: %s...", ctx)
                    if ctx == "health":
                        report[ctx] = analyzer.analyze_health()
                    elif ctx == "security":
                        report[ctx] = analyzer.analyze_security()
                    elif ctx == "capacity":
                        report[ctx] = analyzer.analyze_capacity()
                except Exception as e:
                    logger.error("Falha ao gerar relatório de %s devido a erros na IA: %s", ctx, e)
                    report[ctx] = f"Análise de {ctx} indisponível no momento."
            
            logger.info("Relatório gerado com sucesso.")
            print(json.dumps(report, indent=2))
            
        except Exception as e:
            logger.error("Erro generalizado na execução da aplicação: %s", e, exc_info=True)
            sys.exit(1)


def main():
    # Injeta variáveis de ambiente de arquivo base, permitindo gerência SRE mais flexível
    load_dotenv()
    
    app = OllamaAnalyzerApp()
    app.run()


if __name__ == "__main__":
    main()
