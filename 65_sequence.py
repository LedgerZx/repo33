import random

def generate_random_sequence(seed, length=10):
    """
    Generate a sequence of random numbers using a given seed.

    :param seed: The seed value for the random number generator.
    :param length: The length of the random sequence to generate.
    :return: A list of random numbers.
    """
    random.seed(seed)
    return [random.randint(1, 100) for _ in range(length)]

def main():
    # Define a list of different seeds
    seeds = [42, 101, 202, 303, 404]

    # Generate and print random sequences for each seed
    for seed in seeds:
        print(f"Random sequence with seed {seed}:")
        sequence = generate_random_sequence(seed)
        print(sequence)
        print()

    # Demonstrate the effect of changing the seed
    print("Demonstrating the effect of changing the seed:")
    print("First sequence with seed 42:")
    first_sequence = generate_random_sequence(42)
    print(first_sequence)

    print("\nSecond sequence with seed 42 (should be the same as the first):")
    second_sequence = generate_random_sequence(42)
    print(second_sequence)

    print("\nThird sequence with seed 101 (different from the first two):")
    third_sequence = generate_random_sequence(101)
    print(third_sequence)

if __name__ == "__main__":
    main()
