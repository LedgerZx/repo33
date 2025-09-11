class Dog:
    def __init__(self, name, breed, age, description):
        self.name = name
        self.breed = breed
        self.age = age
        self.description = description
        self.is_adopted = False

    def __str__(self):
        return f"Name: {self.name}, Breed: {self.breed}, Age: {self.age}, Description: {self.description}"

class DogAdoptionAgency:
    def __init__(self):
        self.dogs = []

    def add_dog(self, name, breed, age, description):
        new_dog = Dog(name, breed, age, description)
        self.dogs.append(new_dog)
        print(f"Added {name} to the adoption agency.")

    def view_available_dogs(self):
        if not self.dogs:
            print("No dogs are currently available for adoption.")
        else:
            print("Available dogs for adoption:")
            for dog in self.dogs:
                if not dog.is_adopted:
                    print(dog)

    def adopt_dog(self, name):
        for dog in self.dogs:
            if dog.name == name and not dog.is_adopted:
                dog.is_adopted = True
                print(f"{name} has been adopted!")
                return
        print(f"No dog named {name} is available for adoption.")

def main():
    agency = DogAdoptionAgency()

    while True:
        print("\nDog Adoption Agency Menu:")
        print("1. Add a dog")
        print("2. View available dogs")
        print("3. Adopt a dog")
        print("4. Exit")

        choice = input("Enter your choice (1/2/3/4): ")

        if choice == '1':
            name = input("Enter the dog's name: ")
            breed = input("Enter the dog's breed: ")
            age = input("Enter the dog's age: ")
            description = input("Enter a short description of the dog: ")
            agency.add_dog(name, breed, age, description)

        elif choice == '2':
            agency.view_available_dogs()

        elif choice == '3':
            name = input("Enter the name of the dog you want to adopt: ")
            agency.adopt_dog(name)

        elif choice == '4':
            print("Thank you for using the Dog Adoption Agency!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
