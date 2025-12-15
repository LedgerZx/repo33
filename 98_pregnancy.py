import datetime
from dateutil.relativedelta import relativedelta

class PregnancyTracker:
    def __init__(self, last_period_date):
        self.last_period_date = last_period_date
        self.conception_date = last_period_date + datetime.timedelta(days=14)
        self.due_date = last_period_date + datetime.timedelta(days=280)  # 40 weeks
        
    def current_week(self):
        today = datetime.date.today()
        days_pregnant = (today - self.conception_date).days
        return max(0, min(40, days_pregnant // 7))
    
    def current_trimester(self):
        week = self.current_week()
        if week <= 13:
            return "First Trimester"
        elif week <= 27:
            return "Second Trimester"
        else:
            return "Third Trimester"
    
    def fetal_development(self):
        week = self.current_week()
        developments = {
            4: "Embryo is the size of a poppy seed",
            8: "Baby is the size of a raspberry, organs forming",
            12: "Baby is the size of a lime, can make fists",
            16: "Baby is the size of an avocado, can suck thumb",
            20: "Baby is the size of a banana, can hear sounds",
            24: "Baby is the size of an ear of corn, lungs developing",
            28: "Baby is the size of an eggplant, can open eyes",
            32: "Baby is the size of a squash, practicing breathing",
            36: "Baby is the size of a honeydew melon, gaining weight",
            40: "Baby is the size of a watermelon, ready for birth"
        }
        
        closest_week = max([w for w in developments if w <= week])
        return developments.get(closest_week, "Early development stage")
    
    def weight_gain_tracker(self, pre_pregnancy_weight):
        week = self.current_week()
        if week <= 12:
            expected_gain = 2 to 4 pounds
        elif week <= 28:
            expected_gain = 10 to 14 pounds
        else:
            expected_gain = 25 to 35 pounds
        
        return f"Expected total weight gain by week {week}: {expected_gain} lbs"
    
    def symptoms_by_trimester(self):
        trimester = self.current_trimester()
        symptoms = {
            "First Trimester": [
                "Morning sickness (nausea)",
                "Fatigue",
                "Frequent urination",
                "Breast tenderness",
                "Food cravings/aversions"
            ],
            "Second Trimester": [
                "Increased energy",
                "Growing belly",
                "Backaches",
                "Dizziness",
                "Linea nigra (dark line on belly)"
            ],
            "Third Trimester": [
                "Braxton Hicks contractions",
                "Shortness of breath",
                "Swelling (edema)",
                "Nesting instinct",
                "Frequent urination (baby pressing bladder)"
            ]
        }
        return symptoms.get(trimester, [])
    
    def countdown_to_due_date(self):
        today = datetime.date.today()
        days_remaining = (self.due_date - today).days
        weeks_remaining = days_remaining // 7
        
        if days_remaining < 0:
            return "Baby should be here already!"
        elif days_remaining == 0:
            return "Today's your due date!"
        else:
            return f"{weeks_remaining} weeks and {days_remaining % 7} days until due date"
    
    def nutrition_needs(self):
        week = self.current_week()
        base_calories = 2000
        
        if week <= 12:
            extra_calories = 300
        elif week <= 28:
            extra_calories = 350
        else:
            extra_calories = 450
        
        return {
            "daily_calories": base_calories + extra_calories,
            "protein": "70-100g daily",
            "iron": "27mg daily (prenatal vitamin)",
            "calcium": "1000mg daily",
            "folic_acid": "600-800mcg daily",
            "water": "8-10 glasses daily"
        }
    
    def pregnancy_milestones(self):
        week = self.current_week()
        milestones = []
        
        if week >= 6:
            milestones.append("Heartbeat detectable by ultrasound")
        if week >= 10:
            milestones.append("Risk of miscarriage significantly reduced")
        if week >= 12:
            milestones.append("End of first trimester")
        if week >= 20:
            milestones.append("Halfway point - baby's sex can be determined")
        if week >= 24:
            milestones.append("Baby is viable (could survive outside womb)")
        if week >= 28:
            milestones.append("Third trimester begins")
        if week >= 37:
            milestones.append("Full term - baby could arrive any day")
        if week >= 40:
            milestones.append("Due date reached")
            
        return milestones

def main():
    print("🤰 Pregnancy Tracker 🤰")
    print("=" * 30)
    
    # Get user input
    last_period_str = input("Enter the first day of your last menstrual period (YYYY-MM-DD): ")
    last_period_date = datetime.datetime.strptime(last_period_str, "%Y-%m-%d").date()
    
    pre_pregnancy_weight = float(input("Enter your pre-pregnancy weight (lbs): "))
    
    # Create tracker instance
    tracker = PregnancyTracker(last_period_date)
    
    # Display information
    print("\n" + "=" * 30)
    print("PREGNANCY STATUS")
    print("=" * 30)
    print(f"Current Week: {tracker.current_week()}")
    print(f"Trimester: {tracker.current_trimester()}")
    print(f"Due Date: {tracker.due_date.strftime('%B %d, %Y')}")
    print(f"Countdown: {tracker.countdown_to_due_date()}")
    
    print("\n" + "=" * 30)
    print("BABY DEVELOPMENT")
    print("=" * 30)
    print(tracker.fetal_development())
    
    print("\n" + "=" * 30)
    print("COMMON SYMPTOMS")
    print("=" * 30)
    for symptom in tracker.symptoms_by_trimester():
        print(f"• {symptom}")
    
    print("\n" + "=" * 30)
    print("NUTRITION NEEDS")
    print("=" * 30)
    nutrition = tracker.nutrition_needs()
    for key, value in nutrition.items():
        print(f"{key.replace('_', ' ').title()}: {value}")
    
    print("\n" + "=" * 30)
    print("MILESTONES REACHED")
    print("=" * 30)
    for milestone in tracker.pregnancy_milestones():
        print(f"✓ {milestone}")
    
    print("\n" + "=" * 30)
    print("WEIGHT GAIN TRACKER")
    print("=" * 30)
    print(tracker.weight_gain_tracker(pre_pregnancy_weight))
    
    print("\n" + "=" * 30)
    print("IMPORTANT DATES")
    print("=" * 30)
    print(f"Last Period: {tracker.last_period_date.strftime('%B %d, %Y')}")
    print(f"Likely Conception: {tracker.conception_date.strftime('%B %d, %Y')}")
    print(f"Due Date: {tracker.due_date.strftime('%B %d, %Y')}")

if __name__ == "__main__":
    main()
