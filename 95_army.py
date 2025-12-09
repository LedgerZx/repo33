import random
import time
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Unit:
    name: str
    health: int
    attack: int
    defense: int
    cost: int
    movement: int = 1

class Army:
    def __init__(self, name: str, resources: int = 1000):
        self.name = name
        self.resources = resources
        self.units: List[Unit] = []
        self.wins = 0
        self.losses = 0
        
    def recruit_unit(self, unit_type: str) -> bool:
        unit_costs = {
            "infantry": Unit("Infantry", 100, 15, 10, 50),
            "archer": Unit("Archer", 80, 20, 5, 75),
            "cavalry": Unit("Cavalry", 150, 25, 15, 150),
            "siege": Unit("Siege Engine", 200, 40, 5, 300)
        }
        
        if unit_type not in unit_costs:
            print(f"Unknown unit type: {unit_type}")
            return False
            
        unit = unit_costs[unit_type]
        if self.resources >= unit.cost:
            self.units.append(unit)
            self.resources -= unit.cost
            print(f"{self.name} recruited {unit.name}! Remaining resources: {self.resources}")
            return True
        else:
            print(f"Not enough resources to recruit {unit.name} (need {unit.cost}, have {self.resources})")
            return False
    
    def battle(self, enemy: 'Army') -> bool:
        print(f"\n{self.name} attacks {enemy.name}!")
        print(f"{self.name} forces: {len(self.units)} units")
        print(f"{enemy.name} forces: {len(enemy.units)} units")
        
        while self.units and enemy.units:
            # Random unit selection from each army
            attacker = random.choice(self.units)
            defender = random.choice(enemy.units)
            
            # Calculate damage
            damage = max(1, attacker.attack - defender.defense)
            defender.health -= damage
            
            print(f"{attacker.name} deals {damage} damage to {defender.name} (HP: {defender.health})")
            
            # Remove dead units
            if defender.health <= 0:
                enemy.units.remove(defender)
                print(f"{defender.name} defeated!")
            
            time.sleep(0.5)  # Pause for readability
        
        if self.units:
            self.wins += 1
            enemy.losses += 1
            loot = random.randint(50, 200)
            self.resources += loot
            print(f"\n{self.name} wins! Gained {loot} resources.")
            return True
        else:
            self.losses += 1
            enemy.wins += 1
            print(f"\n{enemy.name} wins!")
            return False
    
    def status(self):
        print(f"\n{self.name} Army Status:")
        print(f"Resources: {self.resources}")
        print(f"Units: {len(self.units)}")
        print(f"Record: {self.wins}W - {self.losses}L")
        if self.units:
            print("Unit composition:")
            unit_count = {}
            for unit in self.units:
                unit_count[unit.name] = unit_count.get(unit.name, 0) + 1
            for name, count in unit_count.items():
                print(f"  {name}: {count}")

def main():
    print("=== Army Management System ===")
    
    # Create armies
    player = Army("Player", 1000)
    enemy = Army("Enemy", 800)
    
    # Game loop
    while True:
        player.status()
        print("\nOptions:")
        print("1. Recruit Infantry (50 resources)")
        print("2. Recruit Archer (75 resources)")
        print("3. Recruit Cavalry (150 resources)")
        print("4. Recruit Siege Engine (300 resources)")
        print("5. Attack Enemy")
        print("6. Quit")
        
        choice = input("Select option: ").strip()
        
        if choice == "1":
            player.recruit_unit("infantry")
        elif choice == "2":
            player.recruit_unit("archer")
        elif choice == "3":
            player.recruit_unit("cavalry")
        elif choice == "4":
            player.recruit_unit("siege")
        elif choice == "5":
            if player.units:
                player.battle(enemy)
                # Enemy recruits random units between battles
                if random.random() > 0.3 and enemy.resources > 50:
                    unit_types = ["infantry", "archer", "cavalry", "siege"]
                    enemy.recruit_unit(random.choice(unit_types))
            else:
                print("You need units to attack!")
        elif choice == "6":
            print("Thanks for playing!")
            break
        else:
            print("Invalid choice!")
        
        # Check win/loss conditions
        if enemy.losses >= 3:
            print(f"\nVictory! You defeated {enemy.name}!")
            break
        if player.losses >= 3:
            print(f"\nDefeat! {enemy.name} has overwhelmed you!")
            break

if __name__ == "__main__":
    main()
