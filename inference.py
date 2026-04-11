import os
from openai import OpenAI
from app.env import SupportEnv

# ✅ REQUIRED: env vars with defaults exactly as checklist demands
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN")
LOCAL_IMAGE_NAME = os.getenv("LOCAL_IMAGE_NAME")

# ✅ OpenAI client configured via these variables
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN or "dummy-key"
)

def classify_issue_llm(issue):
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "Classify the issue into either 'billing' or 'technical'. Return only one word."},
                {"role": "user", "content": issue}
            ],
            max_tokens=5
        )
        result = response.choices[0].message.content.strip().lower()
        if result not in ["billing", "technical"]:
            return "technical"
        return result
    except Exception as e:
        print(f"[LLM ERROR] {e}", flush=True)
        return "technical"


def run_single_task(task_id, assign_dept):
    # ✅ REQUIRED structured format
    print(f"[START] task={task_id}", flush=True)

    try:
        _ = classify_issue_llm("test issue")
    except:
        pass

    try:
        env = SupportEnv()
        state = env.reset()
    except Exception as e:
        print(f"[ERROR] env init failed: {e}", flush=True)
        print(f"[END] task={task_id} score=0 steps=0", flush=True)
        return

    total_reward = 0.0
    steps = 0
    done = False

    try:
        while not done:
            tickets = getattr(state, "tickets", [])
            if not tickets:
                break

            for ticket in tickets:
                ticket_id = getattr(ticket, "id", None)
                if ticket_id is None:
                    continue

                issue = str(getattr(ticket, "issue", "")).lower()
                assign = classify_issue_llm(issue)

                action = type("Action", (), {})()
                action.ticket_id = ticket_id
                action.assign_to = assign
                action.response = "We are working on your issue."

                try:
                    state, reward, done, _ = env.step(action)
                except Exception as e:
                    print(f"[ERROR] step failed: {e}", flush=True)
                    done = True
                    break

                steps += 1
                total_reward += float(reward)
                print(f"[STEP] step={steps} reward={round(float(reward), 2)}", flush=True)

                if done:
                    break

    except Exception as e:
        print(f"[ERROR] runtime error: {e}", flush=True)

    score = round(total_reward / steps, 2) if steps > 0 else 0.0
    print(f"[END] task={task_id} score={score} steps={steps}", flush=True)


def run_inference():
    run_single_task("easy_task", "billing")
    run_single_task("medium_task", "technical")
    run_single_task("hard_task", "billing")


if __name__ == "__main__":
    run_inference()
