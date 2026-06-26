import pytest
from src.test_case import TestCase

def test_create_and_serialize():
    tc = TestCase(name="Login Test", description="Test login flow", steps=["Open page", "Enter creds"], expected_result="Success")
    d = tc.to_dict()
    assert d["name"] == "Login Test"
    assert d["steps"] == ["Open page", "Enter creds"]
    json_str = tc.to_json()
    assert isinstance(json_str, str)
    tc2 = TestCase.from_json(json_str)
    assert tc2.name == tc.name
    assert tc2.steps == tc.steps

def test_add_empty_step_raises():
    tc = TestCase(name="Empty Step Test")
    with pytest.raises(ValueError):
        tc.add_step("")
