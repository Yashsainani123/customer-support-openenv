from fastapi import FastAPI, HTTPException
from app.env import SupportEnv
from app.models import Action

# ✅ Import the task and grader functions you built in tasks.py
from app.tasks import easy_task, medium_task, hard_task, easy_grader, medium_grader, hard_grader

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

# ✅ Keep the tasks clearly defined
@app.get("/tasks")
def tasks():
    return [
        {"id": "easy_task", "grader": "/grader/easy_task"},
        {"id": "medium_task", "grader": "/grader/medium_task"},
        {"id": "hard_task", "grader": "/grader/hard_task"}
    ]

@app.get("/baseline")
def baseline():
    return {"message": "Baseline agent uses simple keyword matching"}

# ✅ The Fix: Create dynamic grader routing for all 3 tasks
@app.post("/grader/{task_name}")
def grade_task(task_name: str):
    env.reset() # Reset the environment for the grader
    
    if task_name == "easy_task":
        raw_score = easy_task(env)
        final_score = easy_grader(raw_score)
        return {"score": final_score}
        
    elif task_name == "medium_task":
        raw_score = medium_task(env)
        final_score = medium_grader(raw_score)
        return {"score": final_score}
        
    elif task_name == "hard_task":
        raw_score = hard_task(env)
        final_score = hard_grader(raw_score)
        return {"score": final_score}
        
    else:
        raise HTTPException(status_code=404, detail="Task not found")
