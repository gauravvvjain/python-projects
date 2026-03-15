from typing import List, Dict, Any
from executor.sandbox import run_code

class TestCaseResult:
    def __init__(self, passed: bool, status: str, execution_time: float, memory_usage: float, error_message: str = ""):
        self.passed = passed
        self.status = status
        self.execution_time = execution_time
        self.memory_usage = memory_usage
        self.error_message = error_message

class EvaluationResult:
    def __init__(self, overall_status: str, total_time: float, max_memory: float, test_results: List[TestCaseResult]):
        self.overall_status = overall_status
        self.total_time = total_time
        self.max_memory = max_memory
        self.test_results = test_results
        self.passed_count = sum(1 for t in test_results if t.passed)
        self.total_count = len(test_results)

def evaluate_submission(language: str, code: str, test_cases: List[Dict[str, str]], time_limit: float = 2.0, memory_limit_mb: int = 256) -> EvaluationResult:
    """
    Evaluates a piece of code against a list of test cases.
    Each test case is a dictionary with 'input' and 'expected_output'.
    """
    results = []
    total_time = 0.0
    max_memory = 0.0
    overall_status = "ACCEPTED"
    
    for tc in test_cases:
        input_data = tc.get("input", "")
        expected_output = tc.get("expected_output", "").strip()
        
        # Run code in sandbox
        run_res = run_code(language, code, input_data, time_limit, memory_limit_mb)
        
        exec_time = run_res["execution_time"]
        mem_usage = run_res["memory_usage"]
        status = run_res["status"]
        
        total_time += exec_time
        max_memory = max(max_memory, mem_usage)
        
        if status != "ACCEPTED":
            results.append(TestCaseResult(False, status, exec_time, mem_usage, run_res["stderr"]))
            if overall_status == "ACCEPTED":
                overall_status = status
            continue
            
        actual_output = run_res["stdout"].strip()
        
        # Output comparison
        if actual_output == expected_output:
            results.append(TestCaseResult(True, "ACCEPTED", exec_time, mem_usage))
        else:
            results.append(TestCaseResult(False, "WRONG_ANSWER", exec_time, mem_usage, f"Expected: {expected_output}, Got: {actual_output}"))
            if overall_status == "ACCEPTED":
                overall_status = "WRONG_ANSWER"
                
    return EvaluationResult(overall_status, total_time, max_memory, results)
