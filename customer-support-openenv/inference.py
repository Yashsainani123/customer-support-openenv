from app.env import SupportEnv

def run_inference():
    env = SupportEnv()
    state = env.reset()

    total_reward = 0
    steps = 0

    for ticket in state["tickets"]:
        action = {
            "ticket_id": ticket["id"],
            "assign_to": "billing" if "payment" in ticket["issue"] else "technical",
            "response": "We are working on your issue, thank you for your patience."
        }

        obj = type("Action", (), action)

        state, reward, done, _ = env.step(obj)

        total_reward += reward
        steps += 1

    return {"score": round(total_reward / steps, 2)}


if __name__ == "__main__":
    print(run_inference())