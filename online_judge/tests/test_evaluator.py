import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from executor.evaluator import evaluate_submission, EvaluationResult

class TestEvaluator:
    def test_evaluate_accepted(self):
        code = """
import sys
for line in sys.stdin:
    a, b = map(int, line.split())
    print(a + b)
"""
        test_cases = [
            {"input": "1 2\n", "expected_output": "3"},
            {"input": "10 20\n", "expected_output": "30"}
        ]
        
        result = evaluate_submission("python", code, test_cases)
        
        assert result.overall_status == "ACCEPTED"
        assert result.passed_count == 2
        assert result.total_count == 2

    def test_evaluate_wrong_answer(self):
        code = """
import sys
for line in sys.stdin:
    a, b = map(int, line.split())
    print(a * b)  # Bug: multiplication instead of addition
"""
        test_cases = [
            {"input": "1 2\n", "expected_output": "3"},
            {"input": "2 2\n", "expected_output": "4"} # This one will actually pass 2*2 == 2+2
        ]
        
        result = evaluate_submission("python", code, test_cases)
        
        assert result.overall_status == "WRONG_ANSWER"
        assert result.passed_count == 1
        assert result.total_count == 2
