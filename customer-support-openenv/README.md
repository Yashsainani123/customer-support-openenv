# Customer Support OpenEnv

## Highlights

- Real-world customer support simulation
- Dynamic difficulty and SLA-based decision making
- Multi-factor reward system for AI evaluation

## Overview

This project implements a real-world OpenEnv environment that simulates a customer support system where an AI agent learns to efficiently handle support tickets.

The environment exposes standard APIs (`/reset`, `/step`, `/state`) and evaluates the agent using a multi-factor reward system.

---

## Problem Statement

Customer support systems face several challenges:

* Incorrect ticket routing
* Delays in resolving issues (SLA violations)
* Poor response quality
* Uneven workload distribution among agents

These issues lead to poor customer satisfaction and inefficient operations.

---

## Solution

This project models a realistic customer support workflow where an AI agent learns to:

* Assign tickets to the correct department
* Generate meaningful responses
* Resolve issues within SLA deadlines
* Manage agent workload efficiently

---

## Environment Design

### State (Observation)

The environment provides:

* Tickets

  * Issue type (payment, login, bug)
  * Priority (low, medium, high)
  * Deadline (SLA)
  * Status (open/resolved)

* Agents

  * Department (billing / technical)
  * Current workload

* Time

  * Current simulation step

---

### Actions

The agent performs:

* Assign ticket to a department
* Generate a response message

---

### Reward Function

The reward is calculated using multiple factors:

* Correct department assignment: +0.4
* Relevant response (keyword-based): +0.3
* Polite response (e.g., "sorry", "thank you"): +0.1
* SLA compliance (within deadline): +0.2
* Wrong assignment: -0.5
* Poor response: -0.2
* SLA violation: -0.3
* Agent overload: -0.4

Final reward is normalized between 0 and 1.

---

## Tasks

### Easy

Assign correct department

### Medium

Assign and generate meaningful response

### Hard

Handle multiple tickets, SLA deadlines, agent workload, and priority-based scheduling

---

## Key Features

* Dynamic difficulty (easy, medium, hard scenarios)
* SLA-aware scheduling
* Priority and deadline-based decision making
* Keyword-based response evaluation
* Customer satisfaction signals
* Agent workload management
* Multi-step environment simulation

---

## Grader

The `/grader` endpoint:

* Resets the environment
* Simulates agent actions
* Computes average reward
* Returns a final score between 0.0 and 1.0

---

## API Endpoints

* `/reset` → Initialize environment
* `/state` → Get current state
* `/step` → Perform action
* `/tasks` → View task levels
* `/baseline` → Baseline agent info
* `/grader` → Evaluate performance

---

## Run Locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Open:
http://127.0.0.1:8000/docs

---

## Docker

```bash
docker build -t support-env .
docker run -p 7860:7860 support-env
```

---

## Real-World Use Cases

This environment can be used to:

* Train AI agents for customer support automation
* Evaluate decision-making under constraints
* Simulate real-world helpdesk systems
* Benchmark reinforcement learning agents

---

## Conclusion

This OpenEnv environment provides a realistic and dynamic simulation of customer support operations, enabling meaningful evaluation of AI agents.
