from app.env import SupportEnv

def run_baseline():
    env = SupportEnv()
    state = env.reset()

    total_reward = 0
    num_tickets = len(state.tickets)

    for ticket in state.tickets:
        action = {
            "ticket_id": ticket.id,
            "assign_to": "billing" if "payment" in ticket.issue else "technical",
            "response": "We are working on your issue, please wait."
        }

        state, reward, done, _ = env.step(type("obj", (), action))
        total_reward += reward

    avg_score = total_reward / num_tickets
    return round(avg_score, 2)


if __name__ == "__main__":
    print("Baseline Score:", run_baseline())