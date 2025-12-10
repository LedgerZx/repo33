import random
import time
from datetime import datetime, timedelta

class Child:
    """
    Represents a child with various attributes that change over time.
    The core logic for a child's needs and development is encapsulated here.
    """
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.hunger = 50  # 0 is full, 100 is starving
        self.energy = 50  # 0 is exhausted, 100 is full of energy
        self.happiness = 75  # 0 is miserable, 100 is ecstatic
        self.knowledge = 0  # Accumulated knowledge points
        self.trust_level = 75  # 0 is no trust, 100 is absolute trust

    def __str__(self):
        return f"--- {self.name} (Age: {self.age}) ---\nHunger: {self.hunger}%\nEnergy: {self.energy}%\nHappiness: {self.happiness}%\nKnowledge: {self.knowledge}\nTrust: {self.trust_level}%"

    def update_stats(self):
        """Simulates the passage of time and its effect on the child's stats."""
        self.hunger = min(100, self.hunger + random.randint(5, 15))
        self.energy = max(0, self.energy - random.randint(5, 15))
        self.happiness = max(0, self.happiness - random.randint(2, 8))
        # Trust can decay slowly if needs are not met
        if self.hunger > 80 or self.energy < 20:
            self.trust_level = max(0, self.trust_level - random.randint(5, 10))

class Parent:
    """
    Represents the user, the parent, trying to raise the child.
    Manages resources and makes decisions.
    """
    def __init__(self, name, patience=100, money=1000):
        self.name = name
        self.patience = patience  # 0 is stressed out, 100 is zen
        self.money = money
        self.energy = 75 # Parent's own energy

    def __str__(self):
        return f"--- {self.name} (Parent) ---\nPatience: {self.patience}%\nEnergy: {self.energy}%\nMoney: ${self.money}"

class Game:
    """
    The main game engine that orchestrates the simulation.
    """
    def __init__(self):
        print("Welcome to the 'Raising Kids' Simulator!")
        child_name = input("Enter your child's name: ")
        child_age = int(input(f"Enter {child_name}'s starting age: "))
        self.child = Child(child_name, child_age)
        self.parent = Parent(input("Enter your name (the parent's): "))
        self.game_over = False
        self.day = 1

    def display_status(self):
        """Prints the current status of parent and child."""
        print("\n" + "="*40)
        print(f"--- Day {self.day} ---")
        print(self.parent)
        print(self.child)
        print("="*40 + "\n")

    def handle_event(self):
        """Presents a random parenting event and handles the choice."""
        events = {
            "tantrum": {
                "description": f"{self.child.name} is throwing a tantrum in the middle of the grocery store!",
                "choices": {
                    "1": {"action": "Give in and buy the candy", "effect": lambda: self._apply_effect(child_happiness=20, parent_money=-10, parent_patience=-5)},
                    "2": {"action": "Stand firm and leave the store", "effect": lambda: self._apply_effect(child_happiness=-15, child_trust=-10, parent_patience=-15)},
                    "3": {"action": "Try to reason with them", "effect": lambda: self._apply_effect(child_happiness=5, parent_patience=-10, child_knowledge=5)}
                }
            },
            "sick": {
                "description": f"Oh no! {self.child.name} woke up with a fever.",
                "choices": {
                    "1": {"action": "Take them to the doctor immediately", "effect": lambda: self._apply_effect(child_happiness=10, child_trust=15, parent_money=-150, parent_patience=-20)},
                    "2": {"action": "Wait and see if it gets better", "effect": lambda: self._apply_effect(parent_patience=-10, child_trust=-5, child_happiness=-5)},
                    "3": {"action": "Give them home remedies and cuddles", "effect": lambda: self._apply_effect(child_trust=10, child_happiness=5, parent_energy=-20)}
                }
            },
            "big_question": {
                "description": f"{self.child.name} asks: 'Where do babies come from?'",
                "choices": {
                    "1": {"action": "Tell the stork story", "effect": lambda: self._apply_effect(child_happiness=10, child_knowledge=-5, child_trust=-5)},
                    "2": {"action": "Give an age-appropriate, honest answer", "effect": lambda: self._apply_effect(child_knowledge=20, child_trust=15, parent_patience=-10)},
                    "3": {"action": "Avoid the question and change the subject", "effect": lambda: self._apply_effect(child_trust=-10, child_happiness=-5)}
                }
            },
            "school_project": {
                "description": f"{self.child.name} has a huge science project due tomorrow!",
                "choices": {
                    "1": {"action": "Do the project for them", "effect": lambda: self._apply_effect(child_happiness=20, child_knowledge=-10, parent_energy=-30)},
                    "2": {"action": "Help them and guide them", "effect": lambda: self._apply_effect(child_knowledge=25, child_trust=10, parent_energy=-20)},
                    "3": {"action": "Let them handle it themselves (tough love)", "effect": lambda: self._apply_effect(child_happiness=-20, child_trust=-15, child_knowledge=10)}
                }
            }
        }
        
        event_type = random.choice(list(events.keys()))
        event = events[event_type]
        
        print(f"\n>>> EVENT: {event['description']}")
        for key, choice in event['choices'].items():
            print(f"  {key}. {choice['action']}")
        
        choice = input("What do you do? (Enter number): ")
        if choice in event['choices']:
            event['choices'][choice]['effect']()
            print("Choice made. Time passes...")
        else:
            print("You hesitated and did nothing, which is also a choice.")
            self.parent.patience -= 5

    def _apply_effect(self, child_happiness=0, child_hunger=0, child_energy=0, child_trust=0, child_knowledge=0, parent_patience=0, parent_money=0, parent_energy=0):
        """Helper function to apply stat changes from an event."""
        self.child.happiness = max(0, min(100, self.child.happiness + child_happiness))
        self.child.hunger = max(0, min(100, self.child.hunger + child_hunger))
        self.child.energy = max(0, min(100, self.child.energy + child_energy))
        self.child.trust_level = max(0, min(100, self.child.trust_level + child_trust))
        self.child.knowledge += child_knowledge
        
        self.parent.patience = max(0, min(100, self.parent.patience + parent_patience))
        self.parent.money += parent_money
        self.parent.energy = max(0, min(100, self.parent.energy + parent_energy))


    def check_game_over(self):
        """Checks for game-over conditions."""
        if self.parent.patience <= 0:
            print("\nGAME OVER: You've run out of patience. You've decided to move to a remote monastery and take up gardening.")
            self.game_over = True
        elif self.parent.money <= 0:
            print("\nGAME OVER: You've run out of money. You had to sell your child to a circus to pay off debts. (Just kidding, you're just really, really broke.)")
            self.game_over = True
        elif self.child.trust_level <= 0:
            print("\nGAME OVER: Your child no longer trusts you. They've decided to go live with their more 'understanding' friend's family.")
            self.game_over = True
        elif self.child.age >= 18:
            self._victory()

    def _victory(self):
        """Checks for victory conditions and displays an ending."""
        print("\n" + "="*40)
        print(f"CONGRATULATIONS! {self.child.name} has turned 18 and is now an adult!")
        print("You have successfully raised your child. Here is the final report:")
        print(self.child)
        print(self.parent)

        # Determine ending based on final stats
        if self.child.happiness > 80 and self.child.knowledge > 100:
            print("\nEnding: The Well-Rounded Success. Your child is happy, smart, and well-adjusted. They credit you for their success.")
        elif self.child.knowledge > 150:
            print("\nEnding: The Academic. Your child is a genius but might be a bit socially awkward. They got a full scholarship to MIT.")
        elif self.child.happiness > 90:
            print("\nEnding: The Happy-Go-Lucky. Your child is full of joy and loves life. They're pursuing their passion for... something. They'll figure it out.")
        elif self.parent.patience < 20:
            print("\nEnding: The Survivor. You made it, but just barely. You and your child have a bond forged in the fires of chaos. You need a long vacation.")
        else:
            print("\nEnding: The Standard Outcome. Your child is... fine. A perfectly normal, average human being. You did okay.")
        
        self.game_over = True


    def run(self):
        """The main game loop."""
        while not self.game_over:
            self.display_status()
            self.handle_event()
            self.child.update_stats()
            self.parent.energy = max(0, self.parent.energy - 5) # Parent gets tired

            # Age the child every 10 days
            if self.day % 10 == 0:
                self.child.age += 1
                print(f"\n>>> {self.child.name} had a birthday! They are now {self.child.age} years old. <<<")
            
            self.day += 1
            time.sleep(2) # Pause for dramatic effect
            self.check_game_over()

if __name__ == "__main__":
    game = Game()
    game.run()
