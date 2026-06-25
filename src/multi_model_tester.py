import json
from dataclasses import dataclass
from datetime import datetime, timedelta
import time

@dataclass
class ProviderMetrics:
    latency: float
    token_usage: int

class MultiModelTester:
    def __init__(self):
        self.results = []

    def record_latency(self, provider_name, start_time, end_time):
        latency = (end_time - start_time).total_seconds()
        return latency

    def extract_token_usage(self, provider_metadata):
        if 'token_usage' in provider_metadata:
            return provider_metadata['token_usage']
        else:
            # Estimate token usage via tokenizers (for simplicity, assume 10 tokens per request)
            return 10

    def store_metrics(self, provider_name, latency, token_usage):
        metrics = ProviderMetrics(latency, token_usage)
        self.results.append({'provider_name': provider_name, 'metrics': metrics.__dict__})

    def display_results(self):
        return json.dumps(self.results, indent=4)

    def test_provider(self, provider_name, provider_metadata):
        start_time = datetime.now()
        # Simulate request processing time (for simplicity, assume 1 second)
        time.sleep(1)
        end_time = datetime.now()
        latency = self.record_latency(provider_name, start_time, end_time)
        token_usage = self.extract_token_usage(provider_metadata)
        self.store_metrics(provider_name, latency, token_usage)
