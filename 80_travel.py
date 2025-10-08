class TravelPlanner:
    def __init__(self):
        self.destinations = {
            "Paris": {"activities": ["Eiffel Tower", "Louvre Museum", "Seine River Cruise"], "budget": 1500},
            "New York": {"activities": ["Statue of Liberty", "Central Park", "Times Square"], "budget": 2000},
            "Tokyo": {"activities": ["Tokyo Tower", "Shibuya Crossing", "Tsukiji Fish Market"], "budget": 2500},
            "Sydney": {"activities": ["Sydney Opera House", "Harbour Bridge", "Bondi Beach"], "budget": 1800},
        }
        self.user_budget = 0
        self.user_destination = ""
        self.user_activities = []

    def choose_destination(self):
        print("Available destinations:")
        for dest in self.destinations:
            print(f"- {dest}")
        self.user_destination = input("Choose your destination: ").strip().capitalize()
        if self.user_destination not in self.destinations:
            print("Invalid destination. Please choose again.")
            self.choose_destination()

    def set_budget(self):
        self.user_budget = float(input("Enter your travel budget: ").strip())
        if self.user_budget < self.destinations[self.user_destination]["budget"]:
            print(f"Your budget is below the recommended budget for {self.user_destination}.")
            self.set_budget()

    def plan_activities(self):
        print(f"Recommended activities in {self.user_destination}:")
        for act in self.destinations[self.user_destination]["activities"]:
            print(f"- {act}")
        self.user_activities = input("Choose your activities (comma-separated): ").strip().split(",")
        for act in self.user_activities:
            act = act.strip().capitalize()
            if act not in self.destinations[self.user_destination]["activities"]:
                print(f"{act} is not a recommended activity in {self.user_destination}. Please choose again.")
                self.plan_activities()
                return
        print(f"Your chosen activities: {', '.join(self.user_activities)}")

    def generate_itinerary(self):
        print("\nYour Travel Itinerary:")
        print(f"Destination: {self.user_destination}")
        print(f"Budget: ${self.user_budget:.2f}")
        print("Activities:")
        for act in self.user_activities:
            print(f"- {act}")

if __name__ == "__main__":
    planner = TravelPlanner()
    planner.choose_destination()
    planner.set_budget()
    planner.plan_activities()
    planner.generate_itinerary()
