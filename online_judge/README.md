# Online Coding Judge Platform

A scalable, distributed platform for evaluating coding submissions, built with Python.

## Components

1. **API Server (FastAPI)**: REST endpoints for users to submit code and WebSockets for real-time status.
2. **Workers (RQ/Redis)**: Scalable backend workers that pick up jobs from the queue.
3. **Execution Engine**: Sandboxed execution environment for running untrusted user code.
4. **Test Case Engine**: Evaluates expected output vs actual output, handles Memory/Time Limit Exceeded.
5. **Ranking Engine**: Custom Priority Queue (MaxHeap) based real-time leaderboard.
6. **PostgreSQL**: Relational storage for users, submissions, and problems.

## Setup Instructions

**Prerequisites:** Docker, Docker Compose, Python 3.10+

1. Install requirements:
```bash
pip install -r requirements.txt
```

2. Start database and queue (Postgres + Redis):
```bash
docker compose up -d
```

3. Start API Server:
```bash
uvicorn api.main:app --reload --port 8000
```

4. Start Worker Node(s):
```bash
python -m workers.worker
```

## Running Tests

We implement several fundamental data structures from scratch. To test them and the execution pipeline:
```bash
pytest tests/
```
