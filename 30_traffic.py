import time

def traffic_light_simulation():
    # Define the states of the traffic light
    states = ["Red", "Green", "Yellow"]

    # Define the duration each light should stay on (in seconds)
    durations = [5, 10, 3]

    while True:
        for state, duration in zip(states, durations):
            print(f"Traffic light is {state}")
            time.sleep(duration)

if __name__ == "__main__":
    traffic_light_simulation()
