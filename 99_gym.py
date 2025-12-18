import json
import datetime
from typing import Dict, List, Optional

class GymMember:
    def __init__(self, member_id: str, name: str, email: str, phone: str):
        self.member_id = member_id
        self.name = name
        self.email = email
        self.phone = phone
        self.membership_start = datetime.date.today()
        self.membership_type = "basic"
        self.workout_history = []
        
    def to_dict(self):
        return {
            "member_id": self.member_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "membership_start": str(self.membership_start),
            "membership_type": self.membership_type,
            "workout_history": self.workout_history
        }

class GymClass:
    def __init__(self, class_id: str, name: str, instructor: str, max_capacity: int):
        self.class_id = class_id
        self.name = name
        self.instructor = instructor
        self.max_capacity = max_capacity
        self.schedule = {}  # Dict of datetime.date to list of time slots
        self.enrolled_members = set()
        
    def add_schedule(self, date: datetime.date, time: str):
        if date not in self.schedule:
            self.schedule[date] = []
        self.schedule[date].append(time)
        
    def enroll_member(self, member_id: str):
        if len(self.enrolled_members) < self.max_capacity:
            self.enrolled_members.add(member_id)
            return True
        return False

class WorkoutSession:
    def __init__(self, member_id: str, exercises: List[Dict]):
        self.member_id = member_id
        self.date = datetime.date.today()
        self.exercises = exercises
        
    def to_dict(self):
        return {
            "member_id": self.member_id,
            "date": str(self.date),
            "exercises": self.exercises
        }

class GymManagementSystem:
    def __init__(self):
        self.members: Dict[str, GymMember] = {}
        self.classes: Dict[str, GymClass] = {}
        self.workout_sessions: List[WorkoutSession] = []
        self.load_data()
        
    def register_member(self, name: str, email: str, phone: str) -> str:
        member_id = f"MEM{len(self.members) + 1:04d}"
        member = GymMember(member_id, name, email, phone)
        self.members[member_id] = member
        self.save_data()
        return member_id
        
    def create_class(self, name: str, instructor: str, max_capacity: int) -> str:
        class_id = f"CLS{len(self.classes) + 1:04d}"
        gym_class = GymClass(class_id, name, instructor, max_capacity)
        self.classes[class_id] = gym_class
        self.save_data()
        return class_id
        
    def log_workout(self, member_id: str, exercises: List[Dict]):
        if member_id not in self.members:
            raise ValueError("Member not found")
            
        session = WorkoutSession(member_id, exercises)
        self.workout_sessions.append(session)
        self.members[member_id].workout_history.append(session.to_dict())
        self.save_data()
        
    def get_member_stats(self, member_id: str) -> Dict:
        if member_id not in self.members:
            return {}
            
        member = self.members[member_id]
        total_workouts = len(member.workout_history)
        
        # Calculate exercise frequency
        exercise_counts = {}
        for session in member.workout_history:
            for exercise in session['exercises']:
                exercise_name = exercise['name']
                exercise_counts[exercise_name] = exercise_counts.get(exercise_name, 0) + 1
                
        return {
            "member_id": member_id,
            "name": member.name,
            "membership_days": (datetime.date.today() - member.membership_start).days,
            "total_workouts": total_workouts,
            "favorite_exercises": sorted(exercise_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        }
        
    def save_data(self):
        data = {
            "members": {mid: m.to_dict() for mid, m in self.members.items()},
            "classes": {cid: {
                "class_id": c.class_id,
                "name": c.name,
                "instructor": c.instructor,
                "max_capacity": c.max_capacity,
                "schedule": {str(k): v for k, v in c.schedule.items()},
                "enrolled_members": list(c.enrolled_members)
            } for cid, c in self.classes.items()},
            "workout_sessions": [s.to_dict() for s in self.workout_sessions]
        }
        
        with open("gym_data.json", "w") as f:
            json.dump(data, f, indent=2)
            
    def load_data(self):
        try:
            with open("gym_data.json", "r") as f:
                data = json.load(f)
                
            # Load members
            for mid, mdata in data.get("members", {}).items():
                member = GymMember(
                    mdata["member_id"],
                    mdata["name"],
                    mdata["email"],
                    mdata["phone"]
                )
                member.membership_start = datetime.datetime.strptime(mdata["membership_start"], "%Y-%m-%d").date()
                member.membership_type = mdata["membership_type"]
                member.workout_history = mdata["workout_history"]
                self.members[mid] = member
                
            # Load classes
            for cid, cdata in data.get("classes", {}).items():
                gym_class = GymClass(
                    cdata["class_id"],
                    cdata["name"],
                    cdata["instructor"],
                    cdata["max_capacity"]
                )
                gym_class.enrolled_members = set(cdata["enrolled_members"])
                for date_str, times in cdata["schedule"].items():
                    date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                    gym_class.schedule[date] = times
                self.classes[cid] = gym_class
                
            # Load workout sessions
            for sdata in data.get("workout_sessions", []):
                session = WorkoutSession(
                    sdata["member_id"],
                    sdata["exercises"]
                )
                session.date = datetime.datetime.strptime(sdata["date"], "%Y-%m-%d").date()
                self.workout_sessions.append(session)
                
        except FileNotFoundError:
            pass  # First time running

def main():
    gym = GymManagementSystem()
    
    while True:
        print("\n=== GYM MANAGEMENT SYSTEM ===")
        print("1. Register new member")
        print("2. Create new class")
        print("3. Log workout session")
        print("4. View member statistics")
        print("5. List all members")
        print("6. List all classes")
        print("7. Exit")
        
        choice = input("Enter your choice (1-7): ")
        
        if choice == "1":
            name = input("Enter member name: ")
            email = input("Enter email: ")
            phone = input("Enter phone: ")
            member_id = gym.register_member(name, email, phone)
            print(f"Member registered successfully! ID: {member_id}")
            
        elif choice == "2":
            name = input("Enter class name: ")
            instructor = input("Enter instructor name: ")
            capacity = int(input("Enter max capacity: "))
            class_id = gym.create_class(name, instructor, capacity)
            print(f"Class created successfully! ID: {class_id}")
            
        elif choice == "3":
            member_id = input("Enter member ID: ")
            exercises = []
            print("Enter exercises (enter 'done' when finished):")
            while True:
                name = input("Exercise name (or 'done'): ")
                if name.lower() == "done":
                    break
                sets = int(input("Sets: "))
                reps = int(input("Reps: "))
                weight = float(input("Weight (kg): "))
                exercises.append({
                    "name": name,
                    "sets": sets,
                    "reps": reps,
                    "weight": weight
                })
            gym.log_workout(member_id, exercises)
            print("Workout logged successfully!")
            
        elif choice == "4":
            member_id = input("Enter member ID: ")
            stats = gym.get_member_stats(member_id)
            if stats:
                print("\n=== MEMBER STATISTICS ===")
                print(f"Name: {stats['name']}")
                print(f"Member ID: {stats['member_id']}")
                print(f"Membership Days: {stats['membership_days']}")
                print(f"Total Workouts: {stats['total_workouts']}")
                print("Favorite Exercises:")
                for exercise, count in stats['favorite_exercises']:
                    print(f"  {exercise}: {count} times")
            else:
                print("Member not found!")
                
        elif choice == "5":
            print("\n=== ALL MEMBERS ===")
            for member in gym.members.values():
                print(f"{member.member_id}: {member.name} ({member.email})")
                
        elif choice == "6":
            print("\n=== ALL CLASSES ===")
            for gym_class in gym.classes.values():
                print(f"{gym_class.class_id}: {gym_class.name} with {gym_class.instructor}")
                print(f"  Capacity: {len(gym_class.enrolled_members)}/{gym_class.max_capacity}")
                
        elif choice == "7":
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
