import random
import time

class Car:
    def __init__(self, name, speed):
        self.name = name
        self.speed = speed
        self.position = 0

    def move(self):
        self.position += self.speed

    def __str__(self):
        return f"{self.name} is at position {self.position}"

def race(car1, car2):
    print(f"Race between {car1.name} and {car2.name} starts!")
    while car1.position < 100 and car2.position < 100:
        car1.move()
        car2.move()
        print(f"{car1} | {car2}")
        time.sleep(0.5)  # Pause to simulate time passing

    if car1.position >= 100 and car2.position >= 100:
        print("It's a tie!")
    elif car1.position >= 100:
        print(f"{car1.name} wins the race!")
    else:
        print(f"{car2.name} wins the race!")

if __name__ == "__main__":
    car1 = Car("Flash", random.randint(1, 5))
    car2 = Car("Zoom", random.randint(1, 5))
    race(car1, car2)
