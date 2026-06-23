import json
from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class TestCase:
    id: int
    prompt: str
    llm_providers: List[str]
    version: str

class MultiModelTester:
    def __init__(self):
        self.test_cases = []
        self.version_counter = 1

    def create_test_case(self, prompt: str, llm_providers: List[str]) -> TestCase:
        if len(llm_providers) < 2:
            raise ValueError("At least two LLM providers are required")
        test_case = TestCase(
            id=len(self.test_cases) + 1,
            prompt=prompt,
            llm_providers=llm_providers,
            version=f"v{self.version_counter}"
        )
        self.test_cases.append(test_case)
        self.version_counter += 1
        return test_case

    def get_test_case(self, test_case_id: int) -> TestCase:
        for test_case in self.test_cases:
            if test_case.id == test_case_id:
                return test_case
        raise ValueError("Test case not found")

    def update_test_case(self, test_case_id: int, prompt: str, llm_providers: List[str]) -> TestCase:
        test_case = self.get_test_case(test_case_id)
        test_case.prompt = prompt
        test_case.llm_providers = llm_providers
        test_case.version = f"v{self.version_counter}"
        self.version_counter += 1
        return test_case

    def delete_test_case(self, test_case_id: int) -> None:
        self.test_cases = [test_case for test_case in self.test_cases if test_case.id != test_case_id]

    def compare_llm_providers(self, test_case_id: int) -> dict:
        test_case = self.get_test_case(test_case_id)
        # Simulate comparison of LLM providers
        comparison_result = {
            "test_case_id": test_case_id,
            "prompt": test_case.prompt,
            "llm_providers": test_case.llm_providers,
            "comparison_result": "LLM provider 1 is better"
        }
        return comparison_result
