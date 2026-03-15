# System Architecture

## Overview
The system relies on asynchronous message passing to decouple the fast API handlers from the slow code execution tasks.

### 1. Submission Flow
`Client -> FastAPI (POST /submit) -> PostgreSQL (Save Status) -> Redis Queue (Enqueue Job) -> Worker Node (Dequeue Job)`

### 2. Execution Flow
`Worker Node -> Code Executor (Sandbox) -> Evaluator -> Update PostgreSQL Status`

### 3. Real-time Status
`Worker Node -> Publish to Redis -> FastAPI WebSocket -> Client`

## Security
User code is run inside a subprocess with `resource` module limits (Time limit, Memory limit). For a true production environment on Linux, `nsjail` or `Docker` should be used instead of standard `subprocess.Popen`.

## Scaling
- **Databases**: Read replicas for heavy fetching of test cases.
- **Workers**: Can easily scale horizontally by adding more process runners listening to the same Redis instance.
- **Queue Priorities**: High queue for fast evaluations, Default for batch jobs.
