import sys
import os

# ✅ Fix path for Hugging Face environment
BASE_DIR = os.path.dirname(__file__)
APP_DIR = os.path.join(BASE_DIR, "app")
sys.path.append(APP_DIR)

# ✅ Safe imports
try:
    from env import SupportEnv
except Exception as e:
    print(f"[IMPORT ERROR] SupportEnv: {e}", flush=True)
    SupportEnv = None

try:
    from models import classify_issue
except Exception as e:
    print(f"[IMPORT ERROR] classify_issue: {e}", flush=True)
    def classify_issue(issue):
        return "general"  # fallback


def run_inference():
    print("[START] task=support_env", flush=True)  # MUST RUN ALWAYS

    # ✅ Safe env initialization
    if SupportEnv is None:
        print("[ERROR] SupportEnv not available", flush=True)
        return {"score": 0.0}

    try:
        env = SupportEnv()
        state = env.reset()
    except Exception as e:
        print(f"[ERROR] env init failed: {e}", flush=True)
        return {"score": 0.0}

    total_reward = 0
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

                # ✅ Safe classification
                try:
                    assign = classify_issue(issue)
                except Exception:
                    assign = "general"

                action = {
                    "ticket_id": ticket_id,
                    "assign_to": assign,
                    "response": "We are working on your issue, thank you for your patience."
                }

                # Convert dict → object (as required)
                obj = type("Action", (), {})()
                for k, v in action.items():
                    setattr(obj, k, v)

                try:
                    state, reward, done, _ = env.step(obj)
                except Exception as e:
                    print(f"[ERROR] step failed: {e}", flush=True)
                    done = True
                    break

                steps += 1
                total_reward += reward

                print(f"[STEP] step={steps} reward={reward}", flush=True)

                if done:
                    break

    except Exception as e:
        print(f"[ERROR] runtime error: {e}", flush=True)

    score = round(total_reward / steps, 2) if steps > 0 else 0.0

    print(f"[END] task=support_env score={score} steps={steps}", flush=True)

    return {"score": score}


if __name__ == "__main__":
    result = run_inference()
    print(result, flush=True)
