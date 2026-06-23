import json
from dataclasses import dataclass
from time import perf_counter
from typing import Dict

@dataclass
class AnthropicResponse:
    response_text: str
    token_usage: int
    latency: float

class AnthropicClient:
    def __init__(self, api_url: str):
        self.api_url = api_url

    def send_prompt(self, prompt: str) -> AnthropicResponse:
        # Simulate API call for demonstration purposes
        start_time = perf_counter()
        response_text = f"Response to: {prompt}"
        token_usage = len(prompt) + len(response_text)
        end_time = perf_counter()
        latency = end_time - start_time
        return AnthropicResponse(response_text, token_usage, latency)

    def get_response(self, prompt: str) -> Dict:
        response = self.send_prompt(prompt)
        return {
            "response_text": response.response_text,
            "token_usage": response.token_usage,
            "latency": response.latency
        }
