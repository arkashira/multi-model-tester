from test_suite import TestSuite, TestCase
import pytest

def test_add_test_case():
    test_suite = TestSuite()
    test_case = TestCase("input", "output", "2022-01-01", "author", ["tag"])
    test_suite.add_test_case(test_case)
    assert len(test_suite.test_cases) == 1
    assert test_suite.test_cases[0].input_prompt == "input"

def test_get_test_cases():
    test_suite = TestSuite()
    test_case1 = TestCase("input1", "output1", "2022-01-01", "author1", ["tag1"])
    test_case2 = TestCase("input2", "output2", "2022-01-02", "author2", ["tag2"])
    test_suite.add_test_case(test_case1)
    test_suite.add_test_case(test_case2)
    assert len(test_suite.get_test_cases()) == 2
    assert len(test_suite.get_test_cases(["tag1"])) == 1

def test_rollback():
    test_suite = TestSuite()
    test_case1 = TestCase("input1", "output1", "2022-01-01", "author1", ["tag1"])
    test_case2 = TestCase("input2", "output2", "2022-01-02", "author2", ["tag2"])
    test_suite.add_test_case(test_case1)
    test_suite.add_test_case(test_case2)
    test_suite.rollback(1)
    assert len(test_suite.test_cases) == 1

def test_to_json():
    test_suite = TestSuite()
    test_case = TestCase("input", "output", "2022-01-01", "author", ["tag"])
    test_suite.add_test_case(test_case)
    json_str = test_suite.to_json()
    assert json_str == '[{"input_prompt": "input", "expected_output": "output", "timestamp": "2022-01-01", "author": "author", "tags": ["tag"]}]'

def test_from_json():
    json_str = '[{"input_prompt": "input", "expected_output": "output", "timestamp": "2022-01-01", "author": "author", "tags": ["tag"]}]'
    test_suite = TestSuite.from_json(json_str)
    assert len(test_suite.test_cases) == 1
    assert test_suite.test_cases[0].input_prompt == "input"

def test_invalid_rollback():
    test_suite = TestSuite()
    with pytest.raises(ValueError):
        test_suite.rollback(1)
