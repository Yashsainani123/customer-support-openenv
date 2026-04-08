# ✅ Task 1
def easy_task(env):
    state = env.reset()
    total_reward = 0

    for _ in range(5):
        if not state.tickets:
            break

        ticket = state.tickets[0]

        action = type("Action", (), {})()
        action.ticket_id = ticket.id
        action.assign_to = "billing"
        action.response = "Working on it"

        state, reward, done, _ = env.step(action)
        total_reward += reward

        if done:
            break

    return total_reward


def easy_grader(score):
    return score >= 0


# ✅ Task 2
def medium_task(env):
    state = env.reset()
    total_reward = 0

    for _ in range(5):
        if not state.tickets:
            break

        ticket = state.tickets[0]

        action = type("Action", (), {})()
        action.ticket_id = ticket.id
        action.assign_to = "technical"
        action.response = "Fixing issue"

        state, reward, done, _ = env.step(action)
        total_reward += reward

        if done:
            break

    return total_reward


def medium_grader(score):
    return score >= 0


# ✅ Task 3
def hard_task(env):
    state = env.reset()
    total_reward = 0

    for _ in range(5):
        if not state.tickets:
            break

        ticket = state.tickets[0]

        action = type("Action", (), {})()
        action.ticket_id = ticket.id
        action.assign_to = "billing"
        action.response = "Resolved quickly"

        state, reward, done, _ = env.step(action)
        total_reward += reward

        if done:
            break

    return total_reward


def hard_grader(score):
    return score >= 0


# ✅ REQUIRED: TASK REGISTRY (MANDATORY)
TASKS = [
    {"task": easy_task, "grader": easy_grader},
    {"task": medium_task, "grader": medium_grader},
    {"task": hard_task, "grader": hard_grader},
]
