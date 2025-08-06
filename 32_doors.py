class SecurityDoor:
    def __init__(self, door_id):
        self.door_id = door_id
        self.is_open = False

    def open(self):
        if not self.is_open:
            self.is_open = True
            print(f"Door {self.door_id} is now open.")
        else:
            print(f"Door {self.door_id} is already open.")

    def close(self):
        if self.is_open:
            self.is_open = False
            print(f"Door {self.door_id} is now closed.")
        else:
            print(f"Door {self.door_id} is already closed.")

    def status(self):
        return self.is_open

class SecuritySystem:
    def __init__(self, door1, door2):
        self.door1 = door1
        self.door2 = door2

    def open_door(self, door_id):
        if door_id == 1:
            if not self.door2.status():
                self.door1.open()
            else:
                print("Cannot open Door 1 while Door 2 is open.")
        elif door_id == 2:
            if not self.door1.status():
                self.door2.open()
            else:
                print("Cannot open Door 2 while Door 1 is open.")
        else:
            print("Invalid door ID.")

    def close_door(self, door_id):
        if door_id == 1:
            self.door1.close()
        elif door_id == 2:
            self.door2.close()
        else:
            print("Invalid door ID.")

    def check_status(self):
        print(f"Door 1 status: {'Open' if self.door1.status() else 'Closed'}")
        print(f"Door 2 status: {'Open' if self.door2.status() else 'Closed'}")

# Example usage:
door1 = SecurityDoor(1)
door2 = SecurityDoor(2)
system = SecuritySystem(door1, door2)

# Open Door 1
system.open_door(1)

# Try to open Door 2 while Door 1 is open
system.open_door(2)

# Close Door 1
system.close_door(1)

# Open Door 2
system.open_door(2)

# Check the status of both doors
system.check_status()
