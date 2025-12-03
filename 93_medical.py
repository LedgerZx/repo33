import json
from datetime import datetime

class MedicalDiagnosisSimulator:
    def __init__(self):
        self.symptoms_db = {
            "fever": {
                "common_cold": 0.7,
                "flu": 0.8,
                "covid19": 0.9,
                "pneumonia": 0.6
            },
            "cough": {
                "common_cold": 0.8,
                "flu": 0.7,
                "covid19": 0.8,
                "pneumonia": 0.9,
                "bronchitis": 0.8
            },
            "headache": {
                "common_cold": 0.5,
                "flu": 0.6,
                "covid19": 0.4,
                "migraine": 0.9,
                "tension_headache": 0.8
            },
            "fatigue": {
                "common_cold": 0.6,
                "flu": 0.8,
                "covid19": 0.9,
                "anemia": 0.7,
                "mononucleosis": 0.8
            },
            "sore_throat": {
                "common_cold": 0.8,
                "flu": 0.5,
                "covid19": 0.6,
                "strep_throat": 0.9
            },
            "shortness_of_breath": {
                "covid19": 0.7,
                "pneumonia": 0.8,
                "asthma": 0.9,
                "anxiety": 0.5
            },
            "chest_pain": {
                "heart_attack": 0.9,
                "pneumonia": 0.6,
                "anxiety": 0.4,
                "costochondritis": 0.7
            }
        }
        
        self.conditions_info = {
            "common_cold": {
                "description": "Viral infection of upper respiratory tract",
                "urgency": "low",
                "recommendation": "Rest, fluids, over-the-counter meds"
            },
            "flu": {
                "description": "Influenza virus infection",
                "urgency": "medium",
                "recommendation": "Antiviral meds if early, rest, fluids"
            },
            "covid19": {
                "description": "SARS-CoV-2 virus infection",
                "urgency": "medium",
                "recommendation": "Test, isolate, monitor breathing"
            },
            "pneumonia": {
                "description": "Lung infection (bacterial or viral)",
                "urgency": "high",
                "recommendation": "Medical evaluation, possible antibiotics"
            },
            "migraine": {
                "description": "Neurovascular headache disorder",
                "urgency": "low",
                "recommendation": "Dark room, pain meds, identify triggers"
            },
            "heart_attack": {
                "description": "Myocardial infarction - medical emergency",
                "urgency": "emergency",
                "recommendation": "CALL 911 IMMEDIATELY - chew aspirin"
            },
            "anxiety": {
                "description": "Psychological condition with physical symptoms",
                "urgency": "low",
                "recommendation": "Breathing exercises, therapy, medication"
            }
        }
    
    def get_symptoms_input(self):
        print("\nEnter symptoms (comma separated, or 'done' to finish):")
        available_symptoms = list(self.symptoms_db.keys())
        print(f"Available symptoms: {', '.join(available_symptoms)}")
        
        symptoms = []
        while True:
            symptom = input("Symptom: ").lower().strip()
            if symptom == "done":
                break
            if symptom in available_symptoms:
                symptoms.append(symptom)
                print(f"Added: {symptom}")
            else:
                print("Not a recognized symptom. Try again.")
        
        return symptoms
    
    def calculate_probabilities(self, symptoms):
        condition_scores = {}
        
        for symptom in symptoms:
            if symptom in self.symptoms_db:
                for condition, prob in self.symptoms_db[symptom].items():
                    if condition not in condition_scores:
                        condition_scores[condition] = []
                    condition_scores[condition].append(prob)
        
        final_scores = {}
        for condition, scores in condition_scores.items():
            # Average probability across all symptoms
            avg_score = sum(scores) / len(scores)
            # Boost score if multiple symptoms match
            boost_factor = 1 + (len(scores) - 1) * 0.1
            final_scores[condition] = min(avg_score * boost_factor, 1.0)
        
        return final_scores
    
    def generate_report(self, symptoms, probabilities):
        report = {
            "timestamp": datetime.now().isoformat(),
            "symptoms": symptoms,
            "possible_conditions": []
        }
        
        # Sort by probability
        sorted_conditions = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)
        
        for condition, prob in sorted_conditions:
            if prob > 0.3:  # Only show conditions with >30% probability
                info = self.conditions_info.get(condition, {
                    "description": "Unknown condition",
                    "urgency": "unknown",
                    "recommendation": "Consult healthcare provider"
                })
                
                report["possible_conditions"].append({
                    "condition": condition.replace("_", " ").title(),
                    "probability": f"{prob:.1%}",
                    "description": info["description"],
                    "urgency": info["urgency"],
                    "recommendation": info["recommendation"]
                })
        
        return report
    
    def save_report(self, report):
        filename = f"medical_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\nReport saved to: {filename}")
    
    def run(self):
        print("=== Medical Diagnosis Simulator ===")
        print("WARNING: This is for educational purposes only!")
        print("Always consult a real healthcare professional for medical concerns.\n")
        
        symptoms = self.get_symptoms_input()
        
        if not symptoms:
            print("No symptoms entered. Exiting.")
            return
        
        probabilities = self.calculate_probabilities(symptoms)
        
        if not probabilities:
            print("No matching conditions found for given symptoms.")
            return
        
        report = self.generate_report(symptoms, probabilities)
        
        print("\n=== DIAGNOSIS REPORT ===")
        print(f"Symptoms: {', '.join(symptoms)}")
        print("\nPossible Conditions:")
        
        for condition in report["possible_conditions"]:
            print(f"\n{condition['condition']} ({condition['probability']})")
            print(f"  Description: {condition['description']}")
            print(f"  Urgency: {condition['urgency']}")
            print(f"  Recommendation: {condition['recommendation']}")
        
        # Emergency check
        emergency_conditions = [c for c in report["possible_conditions"] if c["urgency"] == "emergency"]
        if emergency_conditions:
            print("\n⚠️  EMERGENCY CONDITIONS DETECTED ⚠️")
            print("SEEK IMMEDIATE MEDICAL ATTENTION!")
        
        save = input("\nSave report to file? (y/n): ").lower()
        if save == 'y':
            self.save_report(report)

if __name__ == "__main__":
    simulator = MedicalDiagnosisSimulator()
    simulator.run()
