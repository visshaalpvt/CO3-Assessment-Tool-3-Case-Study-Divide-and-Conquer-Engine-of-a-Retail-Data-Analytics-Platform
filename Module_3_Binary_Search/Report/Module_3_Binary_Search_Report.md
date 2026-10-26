# Module 3: Binary Search for First Occurrence Order Lookup

## 1. Problem Context and Requirements
- **Workload**: High-frequency order lookups over 10,000,000 consolidated orders sorted by timestamp.
- **Key Requirement**: Return the *first* (earliest arrival) record matching a given timestamp when duplicates exist.
- **Limitation of Standard Binary Search**: Standard binary search terminates immediately upon encountering any arbitrary match at `mid`, which may be the 2nd, 3rd, or last duplicate.
- **Linear Scan Inefficiency**: $O(n)$ search across 10 million items requires an average of 5,000,000 comparisons per query, causing database read bottlenecks.

## 2. Divide-and-Conquer Algorithmic Design (Lower-Bound Search)
- **Divide**: Compute midpoint index $mid = low + \lfloor (high - low)/2 \rfloor$.
- **Conquer**:
  - If $A[mid].timestamp \ge target$:
    - If equal, record `answer = mid`.
    - Continue searching left by setting $high = mid - 1$ to verify if an earlier match exists.
  - If $A[mid].timestamp < target$:
    - Discard left half by setting $low = mid + 1$.
- **Combine**: No recombination necessary; the search interval converges to the first occurrence index or terminates with `-1` if not found.

## 3. Sample Execution Trace
- **Sorted Array**: `[(101, 'O4'), (102, 'O2'), (102, 'O5'), (103, 'O6'), (105, 'O1'), (105, 'O3')]`
- **Query 1**: Target = 102
  - $low = 0, high = 5 \implies mid = 2 \rightarrow (102, 'O5')$.
  - $102 \ge 102 \implies answer = 2$, set $high = 1$.
  - $low = 0, high = 1 \implies mid = 0 \rightarrow (101, 'O4')$.
  - $101 < 102 \implies low = 1$.
  - $low = 1, high = 1 \implies mid = 1 \rightarrow (102, 'O2')$.
  - $102 \ge 102 \implies answer = 1$, set $high = 0$.
  - Loop terminates ($low > high$). Returns `index = 1` (`(102, 'O2')`).
- **Query 2**: Target = 104
  - Returns `-1` (Not found).
- **Query 3**: Target = 105
  - Returns `index = 4` (`(105, 'O1')`).

## 4. Recurrence Relation and Complexity Analysis
- **Recurrence**:
  $$T(n) = T(n/2) + \Theta(1), \quad T(1) = \Theta(1)$$
- **Master Theorem Application**:
  - $a = 1, b = 2, f(n) = \Theta(1) = \Theta(n^0)$.
  - $n^{\log_b a} = n^{\log_2 1} = n^0 = 1$.
  - Case 2 applies:
  $$T(n) = \Theta(\log_2 n)$$
- **Space Complexity**: $\Theta(1)$ auxiliary memory (iterative implementation uses constant space).

## 5. Theoretical Calculation for Production Workload ($n = 10,000,000$)
- Maximum binary search decision depth:
  $$\lceil \log_2 (10,000,000 + 1) \rceil = 24 \text{ comparisons}$$
- **Speedup vs Linear Search**:
  $$\frac{5,000,000 \text{ comparisons}}{24 \text{ comparisons}} \approx 208,333\times \text{ latency improvement}$$
- Guaranteed bounded response time $(< 1 \mu s)$ per query.
