import sys
import math
from functools import lru_cache
from itertools import islice
from collections import deque
import time

class PrimeFinder:
    """Optimized prime number generator using multiple performance techniques"""
    
    def __init__(self, limit):
        self.limit = limit
        self._primes_cache = {}
        self._wheel = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        
    @lru_cache(maxsize=1000)
    def _is_prime_cached(self, n):
        """Memoized primality test using wheel factorization"""
        if n < 2:
            return False
        for p in self._wheel:
            if n % p == 0:
                return n == p
        
        # Check up to sqrt(n) using 6k ± 1 optimization
        limit = int(math.isqrt(n))
        for i in range(31, limit + 1, 6):
            if n % i == 0 or n % (i + 2) == 0:
                return False
        return True
    
    def sieve_generator(self):
        """Memory-efficient sieve using generator pattern"""
        sieve = bytearray(b'\x01') * (self.limit + 1)
        sieve[:2] = b'\x00\x00'
        
        for num in range(2, int(math.isqrt(self.limit)) + 1):
            if sieve[num]:
                sieve[num*num:self.limit+1:num] = b'\x00' * len(sieve[num*num:self.limit+1:num])
                yield num
        
        # Yield remaining primes
        for num in range(int(math.isqrt(self.limit)) + 1, self.limit + 1):
            if sieve[num]:
                yield num
    
    def segmented_sieve(self, segment_size=32768):
        """Segmented sieve for very large ranges"""
        # Generate small primes first
        small_primes = list(self.sieve_generator())
        
        # Process in segments to save memory
        for low in range(2, self.limit + 1, segment_size):
            high = min(low + segment_size - 1, self.limit)
            segment = bytearray(b'\x01') * (high - low + 1)
            
            for p in small_primes:
                if p * p > high:
                    break
                start = max(p * p, ((low + p - 1) // p) * p)
                for multiple in range(start, high + 1, p):
                    segment[multiple - low] = 0
            
            for i, is_prime in enumerate(segment):
                if is_prime and (low + i) >= 2:
                    yield low + i
    
    def benchmark_methods(self):
        """Compare different optimization approaches"""
        methods = [
            ("Cached Wheel Factorization", self._test_cached),
            ("Sieve Generator", self._test_sieve),
            ("Segmented Sieve", self._test_segmented)
        ]
        
        print(f"Finding primes up to {self.limit:,}")
        print("-" * 50)
        
        for name, method in methods:
            start = time.perf_counter()
            count = method()
            elapsed = time.perf_counter() - start
            print(f"{name:25} | {count:8,} primes | {elapsed:6.3f}s")
    
    def _test_cached(self):
        """Test cached wheel factorization method"""
        return sum(1 for i in range(2, self.limit + 1) if self._is_prime_cached(i))
    
    def _test_sieve(self):
        """Test sieve generator method"""
        return sum(1 for _ in self.sieve_generator())
    
    def _test_segmented(self):
        """Test segmented sieve method"""
        return sum(1 for _ in self.segmented_sieve())

def demonstrate_optimizations():
    """Show various Python performance optimization techniques"""
    
    # Example 1: Generator for memory efficiency
    def fibonacci_generator(n):
        """Memory-efficient Fibonacci using generators"""
        a, b = 0, 1
        for _ in range(n):
            yield a
            a, b = b, a + b
    
    # Example 2: Pre-allocated list for performance
    def preallocated_list(size):
        """Pre-allocate list to avoid repeated resizing"""
        result = [None] * size
        for i in range(size):
            result[i] = i * i
        return result
    
    # Example 3: Efficient data structures
    def membership_test():
        """Demonstrate set vs list membership performance"""
        data_list = list(range(100000))
        data_set = set(data_list)
        
        test_values = [99999, 50000, 0, 99999]
        
        # List membership (O(n))
        list_time = time.perf_counter()
        for val in test_values:
            val in data_list
        list_time = time.perf_counter() - list_time
        
        # Set membership (O(1))
        set_time = time.perf_counter()
        for val in test_values:
            val in data_set
        set_time = time.perf_counter() - set_time
        
        return list_time, set_time
    
    # Example 4: Bit operations for arithmetic
    def bit_operations():
        """Use bitwise operations for performance"""
        return [
            (x << 1) == x * 2,      # Left shift for multiplication by 2
            (x >> 1) == x // 2,     # Right shift for division by 2
            (x & 1) == x % 2,       # Bitwise AND for even/odd check
            (x ^^ x) == 0            # XOR with self for zero
            for x in range(10)
        ]
    
    # Run demonstrations
    print("Performance Optimization Demonstrations")
    print("=" * 50)
    
    # Test membership efficiency
    list_time, set_time = membership_test()
    print(f"List membership test:  {list_time:.6f}s")
    print(f"Set membership test:   {set_time:.6f}s")
    print(f"Set is {list_time/set_time:.1f}x faster\n")
    
    # Show bit operations
    print("Bit operation equivalences:")
    bit_results = bit_operations()
    print(f"Shift operations work: {all(bit_results[:2])}")
    print(f"Parity check works:    {bit_results[2]}")
    print(f"XOR zero check works:  {bit_results[3]}\n")
    
    # Memory-efficient Fibonacci
    print("First 10 Fibonacci numbers (generator):")
    fib_gen = fibonacci_generator(10)
    print(list(fib_gen))
    print()

if __name__ == "__main__":
    # Demonstrate various optimizations
    demonstrate_optimizations()
    
    # Benchmark prime finding methods
    limit = 100000
    prime_finder = PrimeFinder(limit)
    prime_finder.benchmark_methods()
    
    print("\nOptimization Techniques Demonstrated:")
    print("• Memoization with @lru_cache")
    print("• Generator patterns for memory efficiency")
    print("• Pre-allocation of data structures")
    print("• Efficient data structure selection (sets vs lists)")
    print("• Bitwise operations for arithmetic")
    print("• Algorithmic optimizations (wheel factorization)")
    print("• Segmented processing for large datasets")
    print("• Bytearray for memory-efficient boolean arrays")
