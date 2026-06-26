import pytest
from src.test_manager import TestManager
from src.test_case import TestCase

def test_add_and_remove():
    mgr = TestManager()
    tc = TestCase(name="Sample")
    mgr.add_test(tc)
    assert mgr.list_tests() == ["Sample"]
    mgr.remove_test("Sample")
    assert mgr.list_tests() == []

def test_duplicate_name_raises():
    mgr = TestManager()
    mgr.add_test(TestCase(name="Dup"))
    with pytest.raises(ValueError):
        mgr.add_test(TestCase(name="Dup"))

def test_get_nonexistent_raises():
    mgr = TestManager()
    with pytest.raises(KeyError):
        mgr.get_test("Missing")
