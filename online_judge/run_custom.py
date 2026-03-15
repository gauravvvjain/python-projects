import argparse
import sys
import os
import json
from textwrap import dedent

# Add the project root to the python path so imports work
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from executor.evaluator import evaluate_submission

def main():
    parser = argparse.ArgumentParser(description="Evaluate a python script against test cases.")
    parser.add_argument("file", help="Path to the python file to evaluate")
    parser.add_argument("--tests", help="Optional path to a JSON file containing test cases", default=None)
    
    args = parser.parse_args()
    
    # Read the code from the file
    try:
        with open(args.file, 'r') as f:
            code = f.read()
    except FileNotFoundError:
        print(f"Error: Could not find file '{args.file}'")
        sys.exit(1)
        
    # Load test cases
    test_cases = []
    if args.tests:
        try:
            with open(args.tests, 'r') as f:
                test_cases = json.load(f)
        except Exception as e:
            print(f"Error reading test cases file: {e}")
            sys.exit(1)
    else:
        # Default test cases for a simple A+B problem
        print("No test case file provided. Using default A+B test cases.")
        test_cases = [
            {"input": "1 2\n", "expected_output": "3"},
            {"input": "10 20\n", "expected_output": "30"},
            {"input": "100 200\n", "expected_output": "300"}
        ]
        
    print(f"Evaluating {args.file} against {len(test_cases)} test cases...\n")
    
    # Run evaluation
    result = evaluate_submission("python", code, test_cases)
    
    # Print results
    print("=" * 40)
    print(f"OVERALL STATUS: {result.overall_status}")
    print(f"PASSED:         {result.passed_count} / {result.total_count}")
    print(f"TOTAL TIME:     {result.total_time:.4f}s")
    print(f"MAX MEMORY:     {result.max_memory:.2f} MB")
    print("=" * 40)
    
    for i, test in enumerate(result.test_results):
        status_icon = "✅" if test.passed else "❌"
        print(f"Test Case {i+1}: {test.status} {status_icon}")
        print(f"  Execution Time: {test.execution_time:.4f}s")
        print(f"  Memory Usage:   {test.memory_usage:.2f} MB")
        if not test.passed and test.error_message:
            print(f"  Error details:")
            print(dedent(test.error_message).strip())
        print("-" * 20)
        
if __name__ == "__main__":
    main()
