def run_inference():
    print("[START] task=support_env", flush=True)

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

                issue = str(getattr(ticket, "issue", "")).lower()

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

                steps += 1
                total_reward += reward

                # ✅ REQUIRED FORMAT
                print(f"[STEP] step={steps} reward={reward}", flush=True)

                if done:
                    break

            if done:
                break

    except Exception as e:
        print(f"[ERROR] message={str(e)}", flush=True)

    score = round(total_reward / steps, 2) if steps > 0 else 0.0

    # ✅ REQUIRED FORMAT
    print(f"[END] task=support_env score={score} steps={steps}", flush=True)

    return {"score": score}
