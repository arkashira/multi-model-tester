import json
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict

@dataclass
class TestCase:
    input_prompt: str
    expected_output: str
    timestamp: str
    author: str
    tags: List[str]

class TestSuite:
    def __init__(self):
        self.test_cases = []
        self.version_history = []

    def add_test_case(self, test_case: TestCase):
        self.test_cases.append(test_case)
        self.version_history.append((test_case, datetime.now()))

    def get_test_cases(self, tags: List[str] = None):
        if tags:
            return [test_case for test_case in self.test_cases if any(tag in test_case.tags for tag in tags)]
        return self.test_cases

    def rollback(self, version: int):
        if version < len(self.version_history):
            self.test_cases = [test_case for test_case, _ in self.version_history[:version]]
        else:
            raise ValueError("Invalid version")

    def to_json(self):
        return json.dumps([test_case.__dict__ for test_case in self.test_cases])

    @classmethod
    def from_json(cls, json_str: str):
        test_suite = cls()
        test_cases = json.loads(json_str)
        for test_case in test_cases:
            test_suite.add_test_case(TestCase(**test_case))
        return test_suite
