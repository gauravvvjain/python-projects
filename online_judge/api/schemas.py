from pydantic import BaseModel

class SubmissionCreate(BaseModel):
    problem_id: int
    user_id: int
    language: str = "python"
    code: str

class ProblemResponse(BaseModel):
    id: int
    title: str
    description: str
    difficulty: str
