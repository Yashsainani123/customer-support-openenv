from fastapi import FastAPI, HTTPException
import uvicorn
from app.env import SupportEnv
from app.tasks import easy_task, medium_task, hard_task, easy_grader, medium_grader, hard_grader

app = FastAPI()

# ✅ RESET
@app.post("/reset")
def reset():
    env = SupportEnv()
    return env.reset()

# ✅ STATE
@app.get("/state")
def state():
    env = SupportEnv()
    return env.state()

# ✅ STEP
@app.post("/step")
def step(action: dict):
    env = SupportEnv()
    obj = type("Action", (), action)
    state, reward, done, _ = env.step(obj)
    return {
        "state": state,
        "reward": reward,
        "done": done
    }

# ✅ TASKS (CRITICAL) — added entry_point field
@app.get("/tasks")
@app.post("/tasks")
def tasks():
    return [
        {"id": "easy_task", "entry_point": "/grader/easy_task", "grader": "/grader/easy_task"},
        {"id": "medium_task", "entry_point": "/grader/medium_task", "grader": "/grader/medium_task"},
        {"id": "hard_task", "entry_point": "/grader/hard_task", "grader": "/grader/hard_task"}
    ]

# ✅ GRADERS (CRITICAL) — added GET support alongside POST
@app.get("/grader/{task_name}")
@app.post("/grader/{task_name}")
def grade_task(task_name: str):
    env = SupportEnv()
    if task_name == "easy_task":
        score = easy_grader(easy_task(env))
    elif task_name == "medium_task":
        score = medium_grader(medium_task(env))
    elif task_name == "hard_task":
        score = hard_grader(hard_task(env))
    else:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"score": float(score), "task": task_name}

# ✅ RUN
def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
