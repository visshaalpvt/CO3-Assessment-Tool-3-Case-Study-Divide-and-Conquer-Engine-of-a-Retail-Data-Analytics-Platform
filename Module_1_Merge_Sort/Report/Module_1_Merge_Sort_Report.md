# Module 1: Stable Merge Sort for Nightly Order Consolidation

## 1. Problem Context and Requirements
- **Workload**: 10,000,000 retail order records collected across multiple microservices nightly.
- **Key Requirement**: Strict stability in sorting by order timestamp. Orders arriving at the same millisecond must preserve their original ingestion sequence (gateway FIFO order).
- **Pitfall of Poor Choice**: An unstable sort reorders concurrent transactions, disrupting ledger reconciliation and customer event ordering. Quadratic algorithms ($O(n^2)$) would require $\sim 10^{14}$ operations, drastically missing the batch processing SLA.

## 2. Divide-and-Conquer Algorithmic Design
- **Divide**: Split the array of $n$ order records into two subarrays of size $\lfloor n/2 \rfloor$ and $\lceil n/2 \rceil$.
- **Conquer**: Recursively sort each subarray until base cases ($n \le 1$) are reached.
- **Combine**: Merge the two sorted subarrays into a single sorted array. Stability is strictly guaranteed by using the condition:
  $$\text{if } L[i].timestamp \le R[j].timestamp \implies \text{take } L[i]$$
  This ensures ties always prioritize the record that originated in the left subarray.

## 3. Sample Execution Trace
- **Input**: `[(105, 'O1'), (102, 'O2'), (105, 'O3'), (101, 'O4'), (102, 'O5'), (103, 'O6')]`
- **Divide Steps**:
  - `[O1, O2, O3]` and `[O4, O5, O6]`
  - Left subtree: `[O1]` and `[O2, O3]` $\rightarrow$ `[O2]` and `[O3]`
  - Right subtree: `[O4]` and `[O5, O6]` $\rightarrow$ `[O5]` and `[O6]`
- **Combine / Merge Steps**:
  1. `merge([O2], [O3])` $\rightarrow$ `[(102, 'O2'), (105, 'O3')]`
  2. `merge([O1], [(102, 'O2'), (105, 'O3')])` $\rightarrow$ `[(102, 'O2'), (105, 'O1'), (105, 'O3')]` (Note: $105 \le 105$ selects `O1` before `O3`)
  3. `merge([O5], [O6])` $\rightarrow$ `[(102, 'O5'), (103, 'O6')]`
  4. `merge([O4], [(102, 'O5'), (103, 'O6')])` $\rightarrow$ `[(101, 'O4'), (102, 'O5'), (103, 'O6')]`
  5. Final Merge:
     - Output: `[(101, 'O4'), (102, 'O2'), (102, 'O5'), (103, 'O6'), (105, 'O1'), (105, 'O3')]`
     - Verified: `O2` precedes `O5` (timestamp 102), and `O1` precedes `O3` (timestamp 105).

## 4. Recurrence Relation and Complexity Derivation
- **Recurrence**:
  $$T(n) = 2T(n/2) + \Theta(n), \quad T(1) = \Theta(1)$$
- **Master Theorem Application**:
  - Form: $T(n) = aT(n/b) + f(n)$ with $a = 2, b = 2, f(n) = \Theta(n)$.
  - $n^{\log_b a} = n^{\log_2 2} = n^1 = n$.
  - Since $f(n) = \Theta(n^{\log_b a})$, Case 2 of the Master Theorem applies:
  $$T(n) = \Theta(n \log_2 n)$$
- **Space Complexity**: $\Theta(n)$ auxiliary memory for merging buffers, plus $O(\log n)$ recursion stack.

## 5. Theoretical Calculation for Production Workload ($n = 10,000,000$)
- $n \log_2 n \approx 10^7 \times 23.2535 \approx 232,535,000$ operations.
- Comparison bound: $n \lceil \log_2 n \rceil - 2^{\lceil \log_2 n \rceil} + 1 \approx 233 \times 10^6$ comparisons.
- Memory Requirement: For 10 million order records ($\sim 64$ bytes each), in-memory representation requires $\approx 640$ MB RAM; auxiliary merge buffers require an additional $\approx 640$ MB. Total RAM $\approx 1.28$ GB.

## 6. Recommendations & External Merge Sort
When production dataset size exceeds available JVM/system RAM:
- Divide data into chunks fitting available memory ($\approx 100$ MB chunks).
- In-memory sort each run using Merge Sort and flush sorted runs to disk.
- Perform a $k$-way merge using a min-heap priority queue with buffered I/O streams.
