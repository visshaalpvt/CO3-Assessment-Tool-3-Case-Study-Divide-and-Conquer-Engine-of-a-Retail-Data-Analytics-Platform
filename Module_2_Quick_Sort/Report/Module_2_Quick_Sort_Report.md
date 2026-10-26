# Module 2: Randomized Quick Sort for Live Seller Leaderboard

## 1. Problem Context and Requirements
- **Workload**: 100,000 active seller performance scores updated throughout high-volume flash sales.
- **Key Requirement**: Rapid in-place sorting to refresh leaderboard metrics with low latency.
- **Vulnerability**: Scores arrive in nearly-sorted order from preceding intervals. A standard deterministic Quick Sort (e.g., first or last element pivot) degrades to worst-case quadratic complexity $\Theta(n^2)$.
- **Consequence of Degradation**: Flash sale UI freezes, timeouts on queries, and $\approx 5$ billion comparisons instead of $\approx 1.66$ million.

## 2. Algorithmic Design and Partitioning Strategy
- **Randomized Pivot Selection**: Choose a random pivot index uniformly from $[low, high]$, swap it with $A[high]$, and proceed with standard Lomuto or Hoare partitioning.
- **Divide**: Partition array into elements $\le pivot$ and elements $> pivot$, placing pivot at index $p$.
- **Conquer**: Recursively apply Quick Sort to subproblems $A[low \dots p-1]$ and $A[p+1 \dots high]$.
- **Combine**: Trivial combine step (in-place partitioning guarantees global order upon subproblem resolution).

## 3. Sample Execution Trace
- **Input Scores**: `[42, 17, 63, 8, 55, 29]`
- **Randomized Partition**:
  - Suppose pivot chosen is 42.
  - Subarrays after partitioning around 42:
    - Left ($< 42$): `[17, 8, 29]`
    - Pivot: `42`
    - Right ($> 42$): `[55, 63]`
  - Recursion on Left `[17, 8, 29]`:
    - Pivot 17: partitions into `[8]`, `17`, `[29]`
  - Recursion on Right `[55, 63]`:
    - Partitions into `55`, `[63]`
- **Sorted Output**: `[8, 17, 29, 42, 55, 63]`

## 4. Recurrence Relations and Complexity Analysis
- **Best/Average Case (Balanced Partition)**:
  $$T(n) = 2T(n/2) + \Theta(n) \implies T(n) = \Theta(n \log_2 n)$$
- **Worst Case (Degenerate Partition)**:
  $$T(n) = T(n-1) + \Theta(n) \implies T(n) = \Theta(n^2)$$
- **Expected Time with Randomized Pivot**: Regardless of input distribution (sorted, reverse sorted, or uniform), the expected comparison count is:
  $$E[T(n)] = 2n \ln n \approx 1.386 n \log_2 n = \Theta(n \log n)$$
- **Space Complexity**:
  - In-place data rearrangement: $O(1)$ auxiliary storage.
  - Recursion stack: $O(\log n)$ average, bounded by Introsort limit $2 \lfloor \log_2 n \rfloor$.

## 5. Theoretical Calculation for Production Workload ($n = 100,000$)
- **Deterministic First-Element Pivot Worst Case**:
  $$\frac{n(n-1)}{2} = \frac{100,000 \times 99,999}{2} \approx 4,999,950,000 \text{ comparisons}$$
- **Randomized Expected Case**:
  $$n \log_2 n \approx 100,000 \times 16.6096 \approx 1,660,964 \text{ comparisons}$$
- **Speedup Ratio**: Over $3,000\times$ fewer operations during peak flash sales.

## 6. Recommendations
- Implement Introsort (hybrid of Quick Sort, Heapsort when recursion exceeds $2\log n$, and Insertion Sort for $n < 16$).
- For sparse seller score updates, maintain an incremental Fenwick/Segment Tree or balanced AVL index.
