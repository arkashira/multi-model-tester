from datetime import datetime, timedelta
import json
from multi_model_tester import MultiModelTester, ProviderMetrics

def test_record_latency():
    tester = MultiModelTester()
    start_time = datetime.now()
    end_time = start_time + timedelta(seconds=1)
    latency = tester.record_latency('test_provider', start_time, end_time)
    assert latency == 1.0

def test_extract_token_usage():
    tester = MultiModelTester()
    provider_metadata = {'token_usage': 20}
    token_usage = tester.extract_token_usage(provider_metadata)
    assert token_usage == 20

def test_store_metrics():
    tester = MultiModelTester()
    provider_name = 'test_provider'
    latency = 1.0
    token_usage = 20
    tester.store_metrics(provider_name, latency, token_usage)
    assert len(tester.results) == 1
    assert tester.results[0]['provider_name'] == provider_name
    assert tester.results[0]['metrics']['latency'] == latency
    assert tester.results[0]['metrics']['token_usage'] == token_usage

def test_display_results():
    tester = MultiModelTester()
    provider_name = 'test_provider'
    latency = 1.0
    token_usage = 20
    tester.store_metrics(provider_name, latency, token_usage)
    results = tester.display_results()
    assert json.loads(results)[0]['provider_name'] == provider_name
    assert json.loads(results)[0]['metrics']['latency'] == latency
    assert json.loads(results)[0]['metrics']['token_usage'] == token_usage

def test_test_provider():
    tester = MultiModelTester()
    provider_name = 'test_provider'
    provider_metadata = {}
    tester.test_provider(provider_name, provider_metadata)
    assert len(tester.results) == 1
    assert tester.results[0]['provider_name'] == provider_name
    assert tester.results[0]['metrics']['latency'] > 0
    assert tester.results[0]['metrics']['token_usage'] == 10
