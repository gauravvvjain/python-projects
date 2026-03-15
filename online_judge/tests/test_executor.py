import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from executor.sandbox import run_code

class TestExecutor:
    def test_python_success(self):
        code = "print(input().strip() + ' World')"
        result = run_code("python", code, "Hello")
        
        assert result["status"] == "ACCEPTED"
        assert result["stdout"].strip() == "Hello World"
        assert result["execution_time"] < 1.0

    def test_python_runtime_error(self):
        code = "print(1 / 0)"
        result = run_code("python", code, "")
        
        assert result["status"] == "RUNTIME_ERROR"
        assert "ZeroDivisionError" in result["stderr"]

    def test_python_time_limit_exceeded(self):
        code = "while True: pass"
        # Use a short timeout for tests
        result = run_code("python", code, "", time_limit=0.5)
        
        assert result["status"] == "TIME_LIMIT_EXCEEDED"
