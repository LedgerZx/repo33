def get_rgb_input(component):
    while True:
        try:
            value = int(input(f"Enter the {component} value (0-255): "))
            if 0 <= value <= 255:
                return value
            else:
                print("Value must be between 0 and 255. Please try again.")
        except ValueError:
            print("Invalid input. Please enter an integer value.")

def main():
    red = get_rgb_input("red")
    green = get_rgb_input("green")
    blue = get_rgb_input("blue")

    rgb_color = (red, green, blue)
    print(f"The RGB color is: {rgb_color}")

    # Optionally, you can also print the color in hex format
    hex_color = f'#{red:02X}{green:02X}{blue:02X}'
    print(f"The hex color code is: {hex_color}")

if __name__ == "__main__":
    main()
