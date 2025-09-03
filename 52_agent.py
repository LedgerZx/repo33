import random

class Agent:
    def __init__(self, name, strategy):
        self.name = name
        self.strategy = strategy
        self.score = 0

    def choose(self, opponent):
        if self.strategy == "cooperate":
            return "cooperate"
        elif self.strategy == "defect":
            return "defect"
        elif self.strategy == "random":
            return random.choice(["cooperate", "defect"])
        elif self.strategy == "tit-for-tat":
            if not hasattr(self, 'last_move'):
                self.last_move = "cooperate"
            return opponent.last_move
        else:
            raise ValueError(f"Unknown strategy: {self.strategy}")

    def update_score(self, points):
        self.score += points

def play_game(agent1, agent2, rounds=100):
    for _ in range(rounds):
        choice1 = agent1.choose(agent2)
        choice2 = agent2.choose(agent1)

        if choice1 == "cooperate" and choice2 == "cooperate":
            agent1.update_score(3)
            agent2.update_score(3)
        elif choice1 == "defect" and choice2 == "defect":
            agent1.update_score(1)
            agent2.update_score(1)
        elif choice1 == "cooperate" and choice2 == "defect":
            agent1.update_score(0)
            agent2.update_score(5)
        elif choice1 == "defect" and choice2 == "cooperate":
            agent1.update_score(5)
            agent2.update_score(0)

        agent1.last_move = choice1
        agent2.last_move = choice2

    print(f"{agent1.name} final score: {agent1.score}")
    print(f"{agent2.name} final score: {agent2.score}")

# Example usage:
agent1 = Agent("Agent 1", "tit-for-tat")
agent2 = Agent("Agent 2", "random")

play_game(agent1, agent2)
