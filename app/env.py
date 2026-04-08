import random
from app.env import SupportEnv
from app.models import classify_issue

class SupportEnv:
    def __init__(self):
        self.reset()

    def generate_ticket(self, id):
        issues = ["payment failed", "login error", "app bug"]

        if self.difficulty == "hard":
            priorities = ["high", "high", "medium"]
            deadline_range = (1, 3)
        elif self.difficulty == "medium":
            priorities = ["medium", "high"]
            deadline_range = (2, 5)
        else:
            priorities = ["low", "medium"]
            deadline_range = (4, 7)

        return Ticket(
            id=id,
            issue=random.choice(issues),
            priority=random.choice(priorities),
            deadline=random.randint(*deadline_range),
            status="open"  # ✅ FIXED
        )

    def reset(self):
        self.time = 0
        self.difficulty = random.choice(["easy", "medium", "hard"])

        self.tickets = [self.generate_ticket(i) for i in range(1, 4)]

        self.agents = [
            Agent(id=1, department="billing"),
            Agent(id=2, department="technical"),
        ]

        return self.state()

    def state(self):
        return Observation(
            tickets=self.tickets,
            agents=self.agents,
            time=self.time
        )

    def step(self, action):
        self.time += 1

        ticket_id = getattr(action, "ticket_id", None)
        assign_to = getattr(action, "assign_to", None)

        ticket = next((t for t in self.tickets if t.id == ticket_id), None)
        agent = next((a for a in self.agents if a.department == assign_to), None)

        if not ticket or not agent:
            return self.state(), 0.0, True, {"error": "Invalid action"}

        if getattr(ticket, "status", "open") == "resolved":
            return self.state(), 0.0, False, {"warning": "Already resolved"}

        agent.current_tasks = getattr(agent, "current_tasks", 0) + 1

        reward = calculate_reward(ticket, action, agent, self.time)

        ticket.status = "resolved"

        done = all(getattr(t, "status", "open") == "resolved" for t in self.tickets)

        return self.state(), reward, done, {}
