import json


class Analyzer:
    def __init__(self, zabbix_data: dict, ai_client):
        self.data = zabbix_data
        self.ai = ai_client

    def analyze_health(self) -> str:
        return self.ai.analyze("health", self.data)

    def analyze_security(self) -> str:
        return self.ai.analyze("security", self.data)

    def analyze_capacity(self) -> str:
        return self.ai.analyze("capacity", self.data)
