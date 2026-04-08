# app/tasks.py

# ✅ Task 1
def easy_task(env):
    state = env.reset()
    total_reward = 0.0

    for _ in range(3):
        if not state.tickets:
            break

        ticket = state.tickets[0]

        action = type("Action", (), {})()
        action.ticket_id = ticket.id
        action.assign_to = "billing"
        action.response = "ok"

        state, reward, done, _ = env.step(action)
        total_reward += float(reward)

        if done:
            break

    return float(total_reward)


# ✅ Task 2
def medium_task(env):
    state = env.reset()
    total_reward = 0.0

    for _ in range(3):
        if not state.tickets:
            break

        ticket = state.tickets[0]

        action = type("Action", (), {})()
        action.ticket_id = ticket.id
        action.assign_to = "technical"
        action.response = "ok"

        state, reward, done, _ = env.step(action)
        total_reward += float(reward)

        if done:
            break

    return float(total_reward)


# ✅ Task 3
def hard_task(env):
    state = env.reset()
    total_reward = 0.0

    for _ in range(3):
        if not state.tickets:
            break

        ticket = state.tickets[0]

        action = type("Action", (), {})()
        action.ticket_id = ticket.id
        action.assign_to = "billing"
        action.response = "ok"

        state, reward, done, _ = env.step(action)
        total_reward += float(reward)

        if done:
            break

    return float(total_reward)


# ✅ FIXED GRADERS (STRICTLY BETWEEN 0 AND 1)
def easy_grader(score):
    return max(0.01, min(0.99, float(score) / 10))


def medium_grader(score):
    return max(0.01, min(0.99, float(score) / 10))


def hard_grader(score):
    return max(0.01, min(0.99, float(score) / 10))


# ✅ REQUIRED FORMAT
TASKS = [
    {"name": "easy_task", "task": easy_task, "grader": easy_grader},
    {"name": "medium_task", "task": medium_task, "grader": medium_grader},
    {"name": "hard_task", "task": hard_task, "grader": hard_grader},
]
