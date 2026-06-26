import json
from dataclasses import dataclass, field
from typing import Dict, Any, List

@dataclass
class TestCase:
    """Represents a single test case."""
    name: str
    description: str = ""
    steps: List[str] = field(default_factory=list)
    expected_result: Any = None

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the test case to a dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "steps": self.steps,
            "expected_result": self.expected_result,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "TestCase":
        """Deserialize a dictionary into a TestCase."""
        return TestCase(
            name=data["name"],
            description=data.get("description", ""),
            steps=data.get("steps", []),
            expected_result=data.get("expected_result"),
        )

    def add_step(self, step: str) -> None:
        """Add a step to the test case."""
        if not step:
            raise ValueError("Step cannot be empty")
        self.steps.append(step)

    def to_json(self) -> str:
        """Return JSON representation."""
        return json.dumps(self.to_dict())

    @staticmethod
    def from_json(data: str) -> "TestCase":
        """Create a TestCase from JSON."""
        return TestCase.from_dict(json.loads(data))
