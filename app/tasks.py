# app/tasks.py

def easy_task(env):
    state = env.reset()
    total_reward = 0

    for _ in range(3):
        if not state.tickets:
            break

        ticket = state.tickets[0]

        action = type("Action", (), {})()
        action.ticket_id = ticket.id
        action.assign_to = "billing"
        action.response = "ok"

        state, reward, done, _ = env.step(action)
        total_reward += reward

        if done:
            break

    return total_reward


def easy_grader(score):
    return float(score)


def medium_task(env):
    state = env.reset()
    total_reward = 0

    for _ in range(3):
        if not state.tickets:
            break

        ticket = state.tickets[0]

        action = type("Action", (), {})()
        action.ticket_id = ticket.id
        action.assign_to = "technical"
        action.response = "ok"

        state, reward, done, _ = env.step(action)
        total_reward += reward

        if done:
            break

    return total_reward


def medium_grader(score):
    return float(score)


def hard_task(env):
    state = env.reset()
    total_reward = 0

    for _ in range(3):
        if not state.tickets:
            break

        ticket = state.tickets[0]

        action = type("Action", (), {})()
        action.ticket_id = ticket.id
        action.assign_to = "billing"
        action.response = "ok"

        state, reward, done, _ = env.step(action)
        total_reward += reward

        if done:
            break

    return total_reward


def hard_grader(score):
    return float(score)


# 🔥 IMPORTANT: EXACT FORMAT REQUIRED
TASKS = [
    {"name": "easy", "task": easy_task, "grader": easy_grader},
    {"name": "medium", "task": medium_task, "grader": medium_grader},
    {"name": "hard", "task": hard_task, "grader": hard_grader},
]
