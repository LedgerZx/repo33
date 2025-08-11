class Elevator:
    def __init__(self, total_floors):
        self.total_floors = total_floors
        self.current_floor = 1  # Starting at the ground floor

    def move_to_floor(self, target_floor):
        if 1 <= target_floor <= self.total_floors:
            print(f"Moving from floor {self.current_floor} to floor {target_floor}.")
            self.current_floor = target_floor
            print(f"Arrived at floor {self.current_floor}.")
        else:
            print(f"Error: Floor {target_floor} is out of range. Please select a floor between 1 and {self.total_floors}.")

    def get_current_floor(self):
        return self.current_floor

    def handle_request(self, request_floor):
        if 1 <= request_floor <= self.total_floors:
            print(f"Request received to move to floor {request_floor}.")
            self.move_to_floor(request_floor)
        else:
            print(f"Error: Requested floor {request_floor} is out of range. Please select a floor between 1 and {self.total_floors}.")

# Example usage
if __name__ == "__main__":
    elevator = Elevator(10)  # Create an elevator for a 10-floor building

    # Simulate some requests
    elevator.handle_request(5)
    elevator.handle_request(8)
    elevator.handle_request(3)
    elevator.handle_request(12)  # Out of range request
