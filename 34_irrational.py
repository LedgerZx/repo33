import math

class ArithmeticFunctions:
    def __init__(self):
        pass

    def add(self, a, b):
        """Add two numbers."""
        return a + b

    def subtract(self, a, b):
        """Subtract the second number from the first."""
        return a - b

    def multiply(self, a, b):
        """Multiply two numbers."""
        return a * b

    def divide(self, a, b):
        """Divide the first number by the second."""
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        return a / b

    def square_root(self, a):
        """Calculate the square root of a number."""
        if a < 0:
            raise ValueError("Cannot calculate the square root of a negative number.")
        return math.sqrt(a)

    def pi(self):
        """Return the value of pi."""
        return math.pi

    def euler(self):
        """Return the value of Euler's number (e)."""
        return math.e

# Example usage:
if __name__ == "__main__":
    arith = ArithmeticFunctions()

    # Example with rational numbers
    a = 10
    b = 5
    print(f"Addition: {arith.add(a, b)}")
    print(f"Subtraction: {arith.subtract(a, b)}")
    print(f"Multiplication: {arith.multiply(a, b)}")
    print(f"Division: {arith.divide(a, b)}")

    # Example with irrational numbers
    print(f"Square root of 2: {arith.square_root(2)}")
    print(f"Value of pi: {arith.pi()}")
    print(f"Value of Euler's number: {arith.euler()}")
