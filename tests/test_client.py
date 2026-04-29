import pytest
from unittest.mock import patch, MagicMock
from rapidapi_plugin.client import RapidAPIClient

def test_client_initialization_and_headers():
    client = RapidAPIClient(api_key="secret", host="test.p.rapidapi.com")
    headers = client.get_headers()
    
    assert "X-RapidAPI-Key" in headers
    assert headers["X-RapidAPI-Key"] == "secret"
    assert "X-RapidAPI-Host" in headers
    assert headers["X-RapidAPI-Host"] == "test.p.rapidapi.com"

def test_client_get_request():
    client = RapidAPIClient(api_key="secret", host="test.p.rapidapi.com")
    
    with patch('urllib.request.urlopen') as mock_urlopen:
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"status": "ok", "data": [1,2,3]}'
        mock_response.getcode.return_value = 200
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        result = client.get("/search?q=test")
        
        # Verify URL construction
        call_args = mock_urlopen.call_args[0][0]
        assert call_args.full_url == "https://test.p.rapidapi.com/search?q=test"
        
        # Verify header injection
        assert call_args.headers["X-rapidapi-key"] == "secret"
        
        # Verify JSON parsing
        assert result == {"status": "ok", "data": [1,2,3]}

def test_client_post_request():
    client = RapidAPIClient(api_key="secret", host="test.p.rapidapi.com")
    
    with patch('urllib.request.urlopen') as mock_urlopen:
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"created": true}'
        mock_response.getcode.return_value = 201
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        payload = {"query": "weather", "limit": 5}
        result = client.post("/graphql", payload)
        
        # Verify POST characteristics
        call_args = mock_urlopen.call_args[0][0]
        assert call_args.get_method() == "POST"
        assert call_args.headers["Content-type"] == "application/json"
        assert b'"query": "weather"' in call_args.data
        
        # Verify JSON parsing
        assert result == {"created": True}
