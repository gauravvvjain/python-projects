# Python Projects 

A collection of **advanced Python projects focused on distributed systems, scalable backend architecture, and core computer science algorithms**.

These projects explore how real-world platforms such as search engines, coding platforms, and productivity systems are designed internally.

The repository demonstrates:

- Distributed processing
- Backend system architecture
- Custom data structures
- Search indexing
- Asynchronous worker pipelines
- Secure code execution environments

---

# 📂 Projects Overview

| Project | Description | Core Concepts |
|------|------|------|
| Online Coding Judge | Distributed platform that evaluates user code submissions | Sandbox execution, worker queues |
| Distributed Search Engine | Scalable search engine built from scratch | PageRank, TF-IDF, indexing |
| Smart Task Manager | Full-stack productivity dashboard | OAuth, real-time systems |
| Billing System | GUI-based billing application | Desktop apps |
| Data Processing Pipeline | CSV data processing and visualization | Data pipelines |

---

#  Online Coding Judge

A distributed platform similar to **LeetCode or HackerRank** that automatically evaluates user code submissions.

## System Architecture

Client
│
▼

FastAPI Server
│
▼

Redis Queue
│
▼

Worker Nodes
│
▼

Sandbox Execution Engine
│
▼

PostgreSQL Database

### Key Features

- Distributed code evaluation using **Redis worker queues**
- **Secure sandbox execution environment**
- Real-time submission updates via **WebSockets**
- Automatic validation of outputs against test cases
- Monitoring of **memory usage and execution time**

### Tech Stack

Python  
FastAPI  
Redis  
PostgreSQL  
WebSockets  

### Core Concepts

- Distributed workers
- Asynchronous job processing
- Secure code execution
- Resource isolation

---

#  Distributed Search Engine

A scalable search engine built from scratch to demonstrate **information retrieval systems**.

## Architecture

Web Crawler
│
▼

HTML Parser
│
▼

Document Processor
│
▼

Inverted Index
│
▼

Ranking Engine
│
▼

Search API

### Key Features

- Distributed **web crawler**
- Fast **inverted indexing**
- Search ranking using **PageRank**
- Relevance scoring using **TF-IDF**
- Custom optimized data structures

### Custom Data Structures

- Trie
- Bloom Filter
- LRU Cache
- Graph structures

### Tech Stack

Python  
FastAPI  
Redis  
Graph Algorithms  

### Core Concepts

- Search indexing
- Graph ranking algorithms
- Information retrieval systems

---

# 🗓 Smart Task Manager

A modern productivity dashboard integrating **task management, financial tracking, and calendar synchronization**.

## Architecture

Next.js Frontend
│
▼

Node.js / Express Backend
│
▼

MongoDB Atlas Database
│
▼

Google APIs

### Key Features

- Google OAuth authentication
- Google Calendar synchronization
- Real-time updates using **Socket.io**
- Task and financial transaction management
- Cloud database integration

### Tech Stack

Next.js  
Node.js  
Express  
MongoDB Atlas  
Google OAuth  
Socket.io  

---

#  Python Billing System

A desktop billing application designed to demonstrate **GUI-based software development in Python**.

### Features

- GUI built with **Tkinter**
- Product management
- Invoice generation
- Automatic price calculations

### Tech Stack

Python  
Tkinter  

---

#  Data Processing Pipeline

A data pipeline for **cleaning, analyzing, and visualizing datasets**.

### Features

- CSV dataset ingestion
- Data cleaning and transformation
- Graph-based visualization
- Analytical summaries

### Tech Stack

Python  
Pandas  
Matplotlib  

---

#  Computer Science Concepts Implemented

- Distributed Systems
- Worker Queue Architectures
- Graph Algorithms
- Information Retrieval Systems
- Inverted Indexing
- Ranking Algorithms (PageRank, TF-IDF)
- Secure Code Execution
- Data Pipelines

---

#  Installation

Clone the repository

```bash
git clone https://github.com/gauravvvjain/python-projects.git
cd python-projects

Install dependencies

pip install -r requirements.txt

Run any project

python main.py
```

⸻

# Learning Objectives

This repository explores how to build:
	•	scalable backend systems
	•	distributed processing architectures
	•	production-style APIs
	•	algorithm-heavy software systems

⸻

# Author

Gaurav Jain

Computer Science Student
Backend & Systems Developer

GitHub:
https://github.com/gauravvvjain

⸻

⭐ If you find this project useful, consider starring the repository.

