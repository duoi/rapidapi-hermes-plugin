import pytest
from unittest.mock import patch, MagicMock
import rapidapi_plugin

# We import the internal function directly for testing the logic
from rapidapi_plugin import rapidapi_request

def test_rapidapi_request_missing_key(monkeypatch):
    monkeypatch.delenv("RAPIDAPI_KEY", raising=False)
    
    result = rapidapi_request(
        host="test.p.rapidapi.com", 
        endpoint="/test"
    )
    
    assert result["success"] is False
    assert "RAPIDAPI_KEY environment variable is missing" in result["error"]

def test_rapidapi_request_success(monkeypatch):
    monkeypatch.setenv("RAPIDAPI_KEY", "test-secret-key")
    
    with patch('rapidapi_plugin.client.RapidAPIClient.get') as mock_get:
        mock_get.return_value = {"message": "hello world"}
        
        result = rapidapi_request(
            host="test.p.rapidapi.com", 
            endpoint="/hello"
        )
        
        mock_get.assert_called_once_with("/hello")
        assert result["success"] is True
        assert result["data"] == {"message": "hello world"}

def test_rapidapi_request_post_success(monkeypatch):
    monkeypatch.setenv("RAPIDAPI_KEY", "test-secret-key")
    
    with patch('rapidapi_plugin.client.RapidAPIClient.post') as mock_post:
        mock_post.return_value = {"created": True}
        
        payload = {"foo": "bar"}
        result = rapidapi_request(
            host="test.p.rapidapi.com", 
            endpoint="/create",
            method="POST",
            payload=payload
        )
        
        mock_post.assert_called_once_with("/create", payload)
        assert result["success"] is True
        assert result["data"] == {"created": True}

def test_rapidapi_request_http_error(monkeypatch):
    monkeypatch.setenv("RAPIDAPI_KEY", "test-secret-key")
    
    with patch('rapidapi_plugin.client.RapidAPIClient.get') as mock_get:
        import urllib.error
        mock_get.side_effect = urllib.error.HTTPError(
            url="https://test.p.rapidapi.com/test", 
            code=403, 
            msg="Forbidden", 
            hdrs={}, 
            fp=MagicMock(read=lambda: b'{"message":"You are not subscribed to this API."}')
        )
        
        result = rapidapi_request(
            host="test.p.rapidapi.com", 
            endpoint="/test"
        )
        
        assert result["success"] is False
        assert "403" in result["error"]
        assert "You are not subscribed" in result["error"]
