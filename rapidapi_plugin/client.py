import urllib.request
import json
from typing import Dict, Any, Optional

class RapidAPIClient:
    def __init__(self, api_key: str, host: str):
        self.api_key = api_key
        self.host = host

    def get_headers(self) -> Dict[str, str]:
        return {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": self.host
        }
        
    def get(self, endpoint: str) -> Dict[str, Any]:
        url = f"https://{self.host}{endpoint}"
        req = urllib.request.Request(url, headers=self.get_headers())
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
            
    def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"https://{self.host}{endpoint}"
        headers = self.get_headers()
        headers["Content-Type"] = "application/json"
        
        encoded_data = json.dumps(data).encode('utf-8')
        req = urllib.request.Request(url, data=encoded_data, headers=headers, method="POST")
        
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
