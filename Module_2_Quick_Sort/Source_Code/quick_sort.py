import random
from typing import List, Optional

def quick_sort(values: List[int], seed: Optional[int] = None) -> List[int]:
    """In-place randomized-pivot quicksort; returns the same list."""
    rng = random.Random(seed)
    def partition(a, low, high):
        pivot_idx = rng.randint(low, high)
        a[pivot_idx], a[high] = a[high], a[pivot_idx]
        pivot = a[high]
        i = low
        for j in range(low, high):
            if a[j] <= pivot:
                a[i], a[j] = a[j], a[i]
                i += 1
        a[i], a[high] = a[high], a[i]
        return i
    def sort(a, low, high):
        # Explicit stack avoids Python recursion-depth failures on extreme inputs.
        stack = [(low, high)]
        while stack:
            lo, hi = stack.pop()
            while lo < hi:
                p = partition(a, lo, hi)
                # Process smaller partition immediately to bound stack growth.
                if p - lo < hi - p:
                    if p + 1 < hi: stack.append((p + 1, hi))
                    hi = p - 1
                else:
                    if lo < p - 1: stack.append((lo, p - 1))
                    lo = p + 1
    if len(values) > 1:
        sort(values, 0, len(values) - 1)
    return values

if __name__ == "__main__":
    scores = [42, 17, 63, 8, 55, 29]
    print("Input:", scores)
    print("Sorted:", quick_sort(scores.copy(), seed=7))
