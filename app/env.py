import random
from models import Ticket, Agent, Observation
from reward import calculate_reward

class SupportEnv:
    def __init__(self):
        self.reset()

    # ✅ Dynamic ticket generation based on difficulty
    def generate_ticket(self, id):
        issues = ["payment failed", "login error", "app bug"]

        # 🎯 Difficulty-based logic
        if self.difficulty == "hard":
            priorities = ["high", "high", "medium"]
            deadline_range = (1, 3)

        elif self.difficulty == "medium":
            priorities = ["medium", "high"]
            deadline_range = (2, 5)

        else:  # easy
            priorities = ["low", "medium"]
            deadline_range = (4, 7)

        return Ticket(
            id=id,
            issue=random.choice(issues),
            priority=random.choice(priorities),
            deadline=random.randint(*deadline_range)
        )

    # ✅ Reset environment
    def reset(self):
        self.time = 0

        # 🔥 NEW: dynamic difficulty
        self.difficulty = random.choice(["easy", "medium", "hard"])

        # Generate tickets
        self.tickets = [self.generate_ticket(i) for i in range(1, 4)]

        # Agents
        self.agents = [
            Agent(id=1, department="billing"),
            Agent(id=2, department="technical"),
        ]

        return self.state()

    # ✅ Current state
    def state(self):
        return Observation(
            tickets=self.tickets,
            agents=self.agents,
            time=self.time
        )

    # ✅ Step function (core logic)
    def step(self, action):
        self.time += 1

        ticket = next((t for t in self.tickets if t.id == action.ticket_id), None)
        agent = next((a for a in self.agents if a.department == action.assign_to), None)

        if not ticket or not agent:
            return self.state(), 0.0, True, {"error": "Invalid action"}

        # ❌ Prevent double resolving
        if ticket.status == "resolved":
            return self.state(), 0.0, False, {"warning": "Ticket already resolved"}

        # Update agent workload
        agent.current_tasks += 1

        # Calculate reward
        reward = calculate_reward(ticket, action, agent, self.time)

        # Resolve ticket
        ticket.status = "resolved"

        # Check completion
        done = all(t.status == "resolved" for t in self.tickets)

        return self.state(), reward, done, {}
