import os
from openai import OpenAI
from app.env import SupportEnv

# ✅ Required env variables
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)


def classify_issue(issue):
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "Classify support tickets into 'billing' or 'technical'."},
                {"role": "user", "content": issue}
            ]
        )
        result = response.choices[0].message.content.lower()

        if "billing" in result:
            return "billing"
        return "technical"

    except Exception:
        return "technical"


def run_inference():
    print("START")

    env = SupportEnv()
    state = env.reset()

    total_reward = 0
    steps = 0

    try:
        while True:
            tickets = getattr(state, "tickets", [])
            if not tickets:
                break

            for ticket in tickets:
                ticket_id = getattr(ticket, "id", None)
                if ticket_id is None:
                    continue

                issue = str(getattr(ticket, "issue", ""))

                assign = classify_issue(issue)

                action = {
                    "ticket_id": ticket_id,
                    "assign_to": assign,
                    "response": "We are working on your issue, thank you for your patience."
                }

                obj = type("Action", (), {})()
                for k, v in action.items():
                    setattr(obj, k, v)

                state, reward, done, _ = env.step(obj)

                print(f"STEP: ticket_id={ticket_id}, assign={assign}, reward={reward}")

                total_reward += reward
                steps += 1

                if done:
                    break

            if done:
                break

    except Exception as e:
        print("ERROR:", str(e))

    score = round(total_reward / steps, 2) if steps > 0 else 0.0

    print("END")

    return {"score": score}


if __name__ == "__main__":
    print(run_inference())
