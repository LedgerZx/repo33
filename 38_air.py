class AirConditioner:
    def __init__(self):
        self.state = 'off'  # 'on' or 'off'
        self.temperature = 25  # in Celsius
        self.fan_speed = 'medium'  # 'low', 'medium', or 'high'

    def turn_on(self):
        self.state = 'on'
        print("Air conditioner is now on.")

    def turn_off(self):
        self.state = 'off'
        print("Air conditioner is now off.")

    def set_temperature(self, temp):
        if 16 <= temp <= 30:
            self.temperature = temp
            print(f"Temperature set to {temp}°C.")
        else:
            print("Temperature must be between 16°C and 30°C.")

    def set_fan_speed(self, speed):
        if speed in ['low', 'medium', 'high']:
            self.fan_speed = speed
            print(f"Fan speed set to {speed}.")
        else:
            print("Fan speed must be 'low', 'medium', or 'high'.")

    def display_status(self):
        print(f"Status: {self.state}")
        print(f"Temperature: {self.temperature}°C")
        print(f"Fan Speed: {self.fan_speed}")

def main():
    ac = AirConditioner()

    while True:
        print("\nAir Conditioner Control Panel")
        print("1. Turn On")
        print("2. Turn Off")
        print("3. Set Temperature")
        print("4. Set Fan Speed")
        print("5. Display Status")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            ac.turn_on()
        elif choice == '2':
            ac.turn_off()
        elif choice == '3':
            temp = int(input("Enter temperature (16-30°C): "))
            ac.set_temperature(temp)
        elif choice == '4':
            speed = input("Enter fan speed (low, medium, high): ")
            ac.set_fan_speed(speed)
        elif choice == '5':
            ac.display_status()
        elif choice == '6':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
