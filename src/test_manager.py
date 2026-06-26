from typing import Dict, List
from .test_case import TestCase

class TestManager:
    """Manages a collection of TestCase objects."""
    def __init__(self) -> None:
        self._tests: Dict[str, TestCase] = {}

    def add_test(self, test: TestCase) -> None:
        """Add a test case. Raises if name already exists."""
        if test.name in self._tests:
            raise ValueError(f"Test case '{test.name}' already exists")
        self._tests[test.name] = test

    def remove_test(self, name: str) -> None:
        """Remove a test case by name. Raises if not found."""
        if name not in self._tests:
            raise KeyError(f"Test case '{name}' not found")
        del self._tests[name]

    def get_test(self, name: str) -> TestCase:
        """Retrieve a test case by name. Raises if not found."""
        if name not in self._tests:
            raise KeyError(f"Test case '{name}' not found")
        return self._tests[name]

    def list_tests(self) -> List[str]:
        """Return a list of test case names."""
        return list(self._tests.keys())

    def to_json(self) -> str:
        """Serialize all tests to JSON."""
        return json.dumps([t.to_dict() for t in self._tests.values()])

    @staticmethod
    def from_json(data: str) -> "TestManager":
        """Deserialize JSON into a TestManager."""
        manager = TestManager()
        for item in json.loads(data):
            manager.add_test(TestCase.from_dict(item))
        return manager
