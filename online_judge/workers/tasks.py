import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.session import SessionLocal
from database.models import Submission, Problem, TestCase, StatusEnum
from executor.evaluator import evaluate_submission

def execute_submission_job(submission_id: str, problem_id: int, language: str, code: str):
    """
    Worker task to execute a code submission.
    """
    db = SessionLocal()
    
    try:
        # 1. Update status to RUNNING
        submission = db.query(Submission).filter(Submission.id == submission_id).first()
        if not submission:
            print(f"Submission {submission_id} not found.")
            return
            
        submission.status = StatusEnum.RUNNING
        db.commit()
        
        # 2. Fetch Problem details and Test Cases
        problem = db.query(Problem).filter(Problem.id == problem_id).first()
        test_cases_objs = db.query(TestCase).filter(TestCase.problem_id == problem_id).all()
        
        test_cases = [
            {"input": tc.input_data, "expected_output": tc.expected_output}
            for tc in test_cases_objs
        ]
        
        if not test_cases:
            # Handle case with no test cases gracefully
            submission.status = StatusEnum.ACCEPTED
            submission.execution_time = 0.0
            submission.memory_usage = 0.0
            db.commit()
            return

        # 3. Evaluate code
        time_limit = problem.time_limit if problem else 2.0
        memory_limit = problem.memory_limit if problem else 256
        
        eval_result = evaluate_submission(
            language=language,
            code=code,
            test_cases=test_cases,
            time_limit=time_limit,
            memory_limit_mb=memory_limit
        )
        
        # 4. Save results back to DB
        # Status mappings: Evaluator vs DB Model Status Enum
        try:
            status = StatusEnum(eval_result.overall_status)
        except ValueError:
            status = StatusEnum.RUNTIME_ERROR

        submission.status = status
        submission.execution_time = eval_result.total_time
        submission.memory_usage = eval_result.max_memory
        db.commit()
        
        # Here we could publish an event to Redis pub/sub for WebSockets!
        print(f"Submission {submission_id} evaluated with status {submission.status.value}")
        
    except Exception as e:
        print(f"Failed to execute job for submission {submission_id}: {e}")
        db.rollback()
        
        submission = db.query(Submission).filter(Submission.id == submission_id).first()
        if submission:
            submission.status = StatusEnum.RUNTIME_ERROR
            db.commit()
    finally:
        db.close()
