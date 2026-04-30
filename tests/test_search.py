import pytest
from unittest.mock import patch, MagicMock
from rapidapi_plugin.search import RapidAPISearch

def test_search_request_formatting():
    searcher = RapidAPISearch(cookies="test_cookie", csrf_token="test_csrf")
    
    with patch('urllib.request.urlopen') as mock_urlopen:
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"data": {"products": {"nodes": [{"name": "test API"}]}}}'
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        result = searcher.search("weather", limit=1)
        
        call_args = mock_urlopen.call_args[0][0]
        assert call_args.get_method() == "POST"
        assert call_args.full_url == "https://rapidapi.com/gateway/graphql"
        
        # Verify injected auth
        assert call_args.headers["Cookie"] == "test_cookie"
        assert call_args.headers["Csrf-token"] == "test_csrf"
        assert call_args.headers["Rapid-client"] == "hub-service"
        
        # Verify JSON body structure
        import json
        payload = json.loads(call_args.data.decode('utf-8'))
        assert payload["operationName"] == "searchApis"
        assert payload["variables"]["searchApiWhereInput"]["term"] == "weather"
        assert payload["variables"]["paginationInput"]["first"] == 1
        
        # Verify response parsing
        assert len(result) == 1
        assert result[0]["name"] == "test API"
