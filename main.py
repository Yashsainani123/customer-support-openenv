from fastapi import FastAPI
from app.env import SupportEnv
from app.models import Action

app = FastAPI()
env = SupportEnv()

@app.post("/reset")
def reset():
    return env.reset()

@app.get("/state")
def state():
    return env.state()

@app.post("/step")
def step(action: Action):
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": info
    }

# ✅ TASKS ENDPOINT
@app.get("/tasks")
def tasks():
    return [
        {"name": "easy_task", "goal": "Assign correct department"},
        {"name": "medium_task", "goal": "Assign + good response"},
        {"name": "hard_task", "goal": "Handle SLA, load, multiple tickets"}
    ]

# ✅ BASELINE ENDPOINT
@app.get("/baseline")
def baseline():
    return {"message": "Baseline agent uses simple keyword matching"}

@app.post("/grader")
def grader():
    env.reset()

    total_reward = 0
    steps = 0

    # ✅ Priority + Deadline sorting
    priority_map = {"high": 0, "medium": 1, "low": 2}

    sorted_tickets = sorted(
        env.tickets,
        key=lambda t: (priority_map[t.priority], t.deadline)
    )

    for t in sorted_tickets:

        if "payment" in t.issue:
            response = "We are processing your payment issue, sorry for inconvenience."
            assign_to = "billing"

        elif "login" in t.issue:
            response = "Please reset your password to fix login issue, thank you."
            assign_to = "technical"

        else:
            response = "We are fixing the bug, thank you for reporting."
            assign_to = "technical"

        action = {
            "ticket_id": t.id,
            "assign_to": assign_to,
            "response": response
        }

        obs, reward, done, _ = env.step(type("obj", (), action))
        total_reward += reward
        steps += 1

    score = total_reward / steps

    return {"score": round(score, 2)}