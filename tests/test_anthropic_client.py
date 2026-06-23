import pytest
from anthropic_client import AnthropicClient, AnthropicResponse

@pytest.fixture
def client():
    return AnthropicClient("https://example.com/api")

def test_send_prompt(client):
    prompt = "Hello, world!"
    response = client.send_prompt(prompt)
    assert isinstance(response, AnthropicResponse)
    assert response.response_text.startswith("Response to:")
    assert response.token_usage > 0
    assert response.latency >= 0

def test_get_response(client):
    prompt = "Hello, world!"
    response = client.get_response(prompt)
    assert isinstance(response, dict)
    assert "response_text" in response
    assert "token_usage" in response
    assert "latency" in response
    assert response["response_text"].startswith("Response to:")
    assert response["token_usage"] > 0
    assert response["latency"] >= 0

def test_empty_prompt(client):
    prompt = ""
    response = client.send_prompt(prompt)
    assert isinstance(response, AnthropicResponse)
    assert response.response_text == "Response to: "
    assert response.token_usage == 13  # "Response to: " has 13 characters
    assert response.latency >= 0
