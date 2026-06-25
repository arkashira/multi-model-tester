from multi_model_tester import MultiModelTester, TestResult

def test_run_test():
    tester = MultiModelTester()
    test_case = "test_case_1"
    results = tester.run_test(test_case)
    assert len(results) == 2
    for provider, result in results.items():
        assert isinstance(result, TestResult)
        assert result.response.startswith("Response from")
        assert result.latency > 0
        assert result.token_usage > 0

def test_call_provider_client():
    tester = MultiModelTester()
    test_case = "test_case_1"
    provider = "provider1"
    result = tester.call_provider_client(test_case, provider)
    assert isinstance(result, TestResult)
    assert result.response == f"Response from {provider} for {test_case}"
    assert result.latency == 0.5
    assert result.token_usage == 10

def test_store_results_in_database():
    tester = MultiModelTester()
    test_case = "test_case_1"
    results = {
        "provider1": TestResult("Response from provider1", 0.5, 10),
        "provider2": TestResult("Response from provider2", 0.6, 20)
    }
    tester.store_results_in_database(test_case, results)
    # No assertions, just verify that the method runs without errors
