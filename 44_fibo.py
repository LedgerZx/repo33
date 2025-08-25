import matplotlib.pyplot as plt

def fibonacci(n):
    sequence = [0, 1]
    for i in range(2, n):
        next_value = sequence[-1] + sequence[-2]
        sequence.append(next_value)
    return sequence

def golden_ratio_convergence(fib_sequence):
    ratios = []
    for i in range(2, len(fib_sequence)):
        ratio = fib_sequence[i] / fib_sequence[i - 1]
        ratios.append(ratio)
    return ratios

# Generate the first 20 Fibonacci numbers
fib_sequence = fibonacci(20)

# Calculate the ratios of consecutive Fibonacci numbers
ratios = golden_ratio_convergence(fib_sequence)

# Plot the Fibonacci sequence
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.plot(fib_sequence, marker='o', linestyle='-', color='b')
plt.title('Fibonacci Sequence')
plt.xlabel('Index')
plt.ylabel('Fibonacci Number')

# Plot the convergence to the Golden Ratio
plt.subplot(1, 2, 2)
plt.plot(ratios, marker='o', linestyle='-', color='r')
plt.axhline(y=1.618033988749895, color='g', linestyle='--', label='Golden Ratio')
plt.title('Convergence to the Golden Ratio')
plt.xlabel('Index')
plt.ylabel('Ratio of Consecutive Fibonacci Numbers')
plt.legend()

plt.tight_layout()
plt.show()
