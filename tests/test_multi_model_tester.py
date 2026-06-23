from multi_model_tester import MultiModelTester, TestCase

def test_create_test_case():
    tester = MultiModelTester()
    prompt = "This is a test prompt"
    llm_providers = ["LLM provider 1", "LLM provider 2"]
    test_case = tester.create_test_case(prompt, llm_providers)
    assert test_case.id == 1
    assert test_case.prompt == prompt
    assert test_case.llm_providers == llm_providers
    assert test_case.version == "v1"

def test_get_test_case():
    tester = MultiModelTester()
    prompt = "This is a test prompt"
    llm_providers = ["LLM provider 1", "LLM provider 2"]
    test_case = tester.create_test_case(prompt, llm_providers)
    retrieved_test_case = tester.get_test_case(test_case.id)
    assert retrieved_test_case == test_case

def test_update_test_case():
    tester = MultiModelTester()
    prompt = "This is a test prompt"
    llm_providers = ["LLM provider 1", "LLM provider 2"]
    test_case = tester.create_test_case(prompt, llm_providers)
    updated_prompt = "This is an updated test prompt"
    updated_llm_providers = ["LLM provider 3", "LLM provider 4"]
    updated_test_case = tester.update_test_case(test_case.id, updated_prompt, updated_llm_providers)
    assert updated_test_case.id == test_case.id
    assert updated_test_case.prompt == updated_prompt
    assert updated_test_case.llm_providers == updated_llm_providers
    assert updated_test_case.version == "v2"

def test_delete_test_case():
    tester = MultiModelTester()
    prompt = "This is a test prompt"
    llm_providers = ["LLM provider 1", "LLM provider 2"]
    test_case = tester.create_test_case(prompt, llm_providers)
    tester.delete_test_case(test_case.id)
    assert len(tester.test_cases) == 0

def test_compare_llm_providers():
    tester = MultiModelTester()
    prompt = "This is a test prompt"
    llm_providers = ["LLM provider 1", "LLM provider 2"]
    test_case = tester.create_test_case(prompt, llm_providers)
    comparison_result = tester.compare_llm_providers(test_case.id)
    assert comparison_result["test_case_id"] == test_case.id
    assert comparison_result["prompt"] == prompt
    assert comparison_result["llm_providers"] == llm_providers
    assert comparison_result["comparison_result"] == "LLM provider 1 is better"

def test_create_test_case_with_less_than_two_llm_providers():
    tester = MultiModelTester()
    prompt = "This is a test prompt"
    llm_providers = ["LLM provider 1"]
    try:
        tester.create_test_case(prompt, llm_providers)
        assert False, "Expected ValueError to be raised"
    except ValueError:
        assert True
