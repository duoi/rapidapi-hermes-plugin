import urllib.request
import json
from typing import Dict, Any, List

class RapidAPISearch:
    """Uses RapidAPI's undocumented internal GraphQL endpoint to search for APIs"""
    
    def __init__(self, cookies: str = "", csrf_token: str = ""):
        self.endpoint = "https://rapidapi.com/gateway/graphql"
        self.cookies = cookies
        self.csrf_token = csrf_token
        
    def search(self, term: str, limit: int = 5) -> List[Dict[str, Any]]:
        payload = {
            "query": """query searchApis($searchApiWhereInput: SearchApiWhereInput!, $paginationInput: PaginationInput, $searchApiOrderByInput: SearchApiOrderByInput) {
              products: searchApis(
                where: $searchApiWhereInput
                pagination: $paginationInput
                orderBy: $searchApiOrderByInput
              ) {
                nodes {
                  id
                  name
                  slugifiedName
                  description
                  pricing
                }
              }
            }""",
            "variables": {
                "paginationInput": {"first": limit, "after": ""},
                "searchApiOrderByInput": {"sortingFields": [{"fieldName": "ByRelevance", "by": "ASC"}]},
                "searchApiWhereInput": {"term": term, "tags": []}
            },
            "operationName": "searchApis"
        }
        
        headers = {
            'accept': '*/*',
            'content-type': 'application/json',
            'rapid-client': 'hub-service',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36'
        }
        
        # Inject auth headers if provided (though it sometimes works without them for public APIs)
        if self.cookies:
            headers['cookie'] = self.cookies
        if self.csrf_token:
            headers['csrf-token'] = self.csrf_token
            
        req = urllib.request.Request(self.endpoint, data=json.dumps(payload).encode('utf-8'), headers=headers)
        
        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result.get("data", {}).get("products", {}).get("nodes", [])
        except urllib.error.HTTPError as e:
            raise Exception(f"HTTP {e.code}: {e.read().decode('utf-8')}")
