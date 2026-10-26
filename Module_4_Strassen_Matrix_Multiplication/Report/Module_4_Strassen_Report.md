# Module 4: Strassen's Matrix Multiplication for Recommendation Scores

## 1. Problem Context and Requirements
- **Workload**: Batch matrix multiplication of user affinity ($A$) and item attribute ($B$) matrices of dimension $1024 \times 1024$.
- **Objective**: Reduce the computational complexity of the recommendation scoring engine compared to conventional matrix multiplication ($O(n^3)$).
- **Core Challenge**: While pure Strassen reduces the asymptotic multiplication exponent to $\approx 2.807$, its high addition overhead, submatrix allocation churn, and diminished cache locality cause slowdowns for smaller submatrices.

## 2. Divide-and-Conquer Algorithmic Design
- **Divide**: Partition $n \times n$ matrices $A$ and $B$ into four $(n/2) \times (n/2)$ submatrices:
  $$A = \begin{pmatrix} A_{11} & A_{12} \\ A_{21} & A_{22} \end{pmatrix}, \quad B = \begin{pmatrix} B_{11} & B_{12} \\ B_{21} & B_{22} \end{pmatrix}$$
- **Conquer**: Instead of 8 standard submatrix multiplications, compute 7 auxiliary products:
  - $M_1 = (A_{11} + A_{22})(B_{11} + B_{22})$
  - $M_2 = (A_{21} + A_{22}) B_{11}$
  - $M_3 = A_{11} (B_{12} - B_{22})$
  - $M_4 = A_{22} (B_{21} - B_{11})$
  - $M_5 = (A_{11} + A_{12}) B_{22}$
  - $M_6 = (A_{21} - A_{11})(B_{11} + B_{12})$
  - $M_7 = (A_{12} - A_{22})(B_{21} + B_{22})$
- **Combine**: Recombine submatrices to yield result matrix $C$:
  - $C_{11} = M_1 + M_4 - M_5 + M_7$
  - $C_{12} = M_3 + M_5$
  - $C_{21} = M_2 + M_4$
  - $C_{22} = M_1 - M_2 + M_3 + M_6$
- **Hybrid Threshold**: Fall back to standard cubic multiplication when $n \le cutoff$ (typically $32 \le cutoff \le 64$) to maximize hardware cache locality and eliminate recursive allocation overhead.

## 3. Sample Execution Trace & Verification
- **Sample Input**:
  $$A = \begin{pmatrix} 1 & 7 \\ 3 & 5 \end{pmatrix}, \quad B = \begin{pmatrix} 1 & 3 \\ 7 & 5 \end{pmatrix}$$
- **Calculation**:
  - $M_1 = (1 + 5)(1 + 5) = 6 \times 6 = 36$
  - $M_2 = (3 + 5) \times 1 = 8 \times 1 = 8$
  - $M_3 = 1 \times (3 - 5) = 1 \times (-2) = -2$
  - $M_4 = 5 \times (7 - 1) = 5 \times 6 = 30$
  - $M_5 = (1 + 7) \times 5 = 8 \times 5 = 40$
  - $M_6 = (3 - 1)(1 + 3) = 2 \times 4 = 8$
  - $M_7 = (7 - 5)(7 + 5) = 2 \times 12 = 24$
- **Combined Blocks**:
  - $C_{11} = 36 + 30 - 40 + 24 = 50$
  - $C_{12} = -2 + 40 = 38$
  - $C_{21} = 8 + 30 = 38$
  - $C_{22} = 36 - 8 - 2 + 8 = 34$
- **Output**:
  $$C = \begin{pmatrix} 50 & 38 \\ 38 & 34 \end{pmatrix}$$
- **Verification via Conventional Multiplication**:
  - $C_{11} = (1 \times 1) + (7 \times 7) = 1 + 49 = 50$
  - $C_{12} = (1 \times 3) + (7 \times 5) = 3 + 35 = 38$
  - $C_{21} = (3 \times 1) + (5 \times 7) = 3 + 35 = 38$
  - $C_{22} = (3 \times 3) + (5 \times 5) = 9 + 25 = 34$
  - Outputs match exactly.

## 4. Recurrence Relation and Master Theorem Derivation
- **Recurrence**:
  $$T(n) = 7 T(n/2) + \Theta(n^2), \quad T(1) = \Theta(1)$$
- **Master Theorem Parameters**:
  - $a = 7, b = 2, f(n) = \Theta(n^2)$
  - Critical exponent: $\log_b a = \log_2 7 \approx 2.80735$
  - $n^{\log_b a} = n^{2.80735} > n^2$
  - Since $f(n) = O(n^{\log_2 7 - \epsilon})$ for $\epsilon \approx 0.807$, Case 1 of the Master Theorem applies:
  $$T(n) = \Theta(n^{\log_2 7}) \approx \Theta(n^{2.807})$$
- **Space Complexity**: $\Theta(n^2)$ for intermediate auxiliary matrices across the recursion tree depth $\log_2 n$.

## 5. Theoretical Calculation for Production Matrix ($n = 1024$)
- **Conventional Scalar Multiplications**:
  $$n^3 = 1024^3 = 1,073,741,824 \text{ multiplications}$$
- **Ideal Strassen Multiplications**:
  $$7^{\log_2 1024} = 7^{10} = 282,475,249 \text{ multiplications}$$
- **Multiplication Reduction**:
  $$\frac{1,073,741,824}{282,475,249} \approx 3.801\times \text{ fewer multiplications}$$

## 6. Practical Engineering Considerations
1. **Numerical Stability**: Strassen has slightly weaker backward numerical stability than standard multiplication for ill-conditioned floating-point matrices.
2. **Memory Footprint**: Requires pre-allocating scratch buffers to eliminate garbage collector pauses during high-frequency recommendation passes.
3. **Hybrid Cutoff**: Benchmark hardware to fix cutoff at $n \in [32, 64]$ to leverage BLAS/SIMD register-level parallelism.
