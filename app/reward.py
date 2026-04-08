def response_score(issue, response):
    keywords = {
        "payment": ["payment", "refund", "transaction"],
        "login": ["login", "password", "access"],
        "bug": ["fix", "bug", "issue", "error"]
    }

    issue_key = issue.split()[0]

    if issue_key in keywords:
        for word in keywords[issue_key]:
            if word in response.lower():
                return 0.3

    return -0.2


def satisfaction_score(response):
    if "sorry" in response.lower() or "thank you" in response.lower():
        return 0.1
    return 0


def calculate_reward(ticket, action, agent, current_time):
    score = 0.0

    # ✅ Correct department
    mapping = {
        "payment": "billing",
        "login": "technical",
        "error": "technical",
        "bug": "technical"
    }

    correct_dept = mapping.get(ticket.issue.split()[0], "general")

    if action.assign_to == correct_dept:
        score += 0.4
    else:
        score -= 0.5

    # ✅ Smart response scoring (NLP-like)
    score += response_score(ticket.issue, action.response)

    # ✅ Customer satisfaction bonus
    score += satisfaction_score(action.response)

    # ✅ SLA (deadline check)
    if current_time <= ticket.deadline:
        score += 0.2
    else:
        score -= 0.3

    # ✅ Agent overload penalty
    if agent.current_tasks > 2:
        score -= 0.4

    # Normalize score strictly between 0 and 1 (not including 0 or 1)
    normalized = max(0.01, min(0.99, score))
    return float(normalized)