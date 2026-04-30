import os
import json
import urllib.error
from typing import Dict, Any, Optional

from tools.registry import registry
from .client import RapidAPIClient

def check_rapidapi_requirements() -> bool:
    """Check if the rapidapi plugin has the required environment variables."""
    return bool(os.getenv("RAPIDAPI_KEY"))

def rapidapi_request(
    host: str, 
    endpoint: str, 
    method: str = "GET", 
    payload: Optional[Dict[str, Any]] = None,
    task_id: str = None
) -> Dict[str, Any]:
    """Execute a generic request against a RapidAPI endpoint."""
    
    api_key = os.getenv("RAPIDAPI_KEY")
    if not api_key:
        return {"success": False, "error": "RAPIDAPI_KEY environment variable is missing. Please add it to ~/.hermes/.env"}
        
    client = RapidAPIClient(api_key=api_key, host=host)
    
    try:
        if method.upper() == "GET":
            response = client.get(endpoint)
        elif method.upper() == "POST":
            response = client.post(endpoint, payload or {})
        else:
            return {"success": False, "error": f"Unsupported HTTP method: {method}"}
            
        return {
            "success": True,
            "data": response
        }
        
    except urllib.error.HTTPError as e:
        try:
            error_body = e.read().decode('utf-8')
        except Exception:
            error_body = str(e)
        return {"success": False, "error": f"HTTP {e.code}: {error_body}"}
        
    except Exception as e:
        return {"success": False, "error": str(e)}

registry.register(
    name="rapidapi_request",
    toolset="rapidapi",
    schema={
        "name": "rapidapi_request",
        "description": "Execute a generic request against a RapidAPI endpoint. Automatically handles X-RapidAPI-Key authentication.",
        "parameters": {
            "type": "object",
            "properties": {
                "host": {
                    "type": "string",
                    "description": "The RapidAPI host domain (e.g., 'weatherapi-com.p.rapidapi.com')"
                },
                "endpoint": {
                    "type": "string",
                    "description": "The specific API path to hit (e.g., '/current.json?q=London')"
                },
                "method": {
                    "type": "string",
                    "enum": ["GET", "POST"],
                    "description": "HTTP method to use (defaults to GET)"
                },
                "payload": {
                    "type": "object",
                    "description": "Optional JSON payload for POST requests"
                }
            },
            "required": ["host", "endpoint"]
        }
    },
    handler=lambda args, **kw: json.dumps(rapidapi_request(
        host=args.get("host"),
        endpoint=args.get("endpoint"),
        method=args.get("method", "GET"),
        payload=args.get("payload"),
        task_id=kw.get("task_id")
    )),
    check_fn=check_rapidapi_requirements,
    requires_env=["RAPIDAPI_KEY"],
)

from .search import RapidAPISearch

def search_rapidapi(term: str, limit: int = 5, task_id: str = None) -> Dict[str, Any]:
    """Search the RapidAPI marketplace for APIs by keyword."""
    # We grab the tokens from environment if the user supplied them, otherwise we try anonymously
    cookies = os.getenv("RAPIDAPI_COOKIES", "")
    csrf = os.getenv("RAPIDAPI_CSRF", "")
    
    searcher = RapidAPISearch(cookies=cookies, csrf_token=csrf)
    try:
        results = searcher.search(term, limit)
        return {
            "success": True,
            "data": results
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

registry.register(
    name="search_rapidapi",
    toolset="rapidapi",
    schema={
        "name": "search_rapidapi",
        "description": "Search the RapidAPI marketplace for APIs by keyword to find new endpoints to use.",
        "parameters": {
            "type": "object",
            "properties": {
                "term": {
                    "type": "string",
                    "description": "The search term (e.g. 'weather', 'ebay', 'flight')"
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of results to return (default 5)"
                }
            },
            "required": ["term"]
        }
    },
    handler=lambda args, **kw: json.dumps(search_rapidapi(
        term=args.get("term"),
        limit=args.get("limit", 5),
        task_id=kw.get("task_id")
    )),
    # No check_fn needed because search can often run anonymously, 
    # or the user can inject RAPIDAPI_COOKIES into .env
)
