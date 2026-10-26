# CO3 – Assessment Tool 3: Case Study – Divide-and-Conquer Engine of a Retail Data Analytics Platform (KartIQ)

## Academic Information
- **Course**: CSA06 – Design and Analysis of Algorithms
- **Assessment**: CO3 – Assessment Tool 3 (100 Points)
- **Student Name**: R. Visshaal
- **Registration Number**: 192421025
- **Platform Case Study**: KartIQ Retail Data Analytics Platform

---

## 1. Project Overview & Objectives
KartIQ is an enterprise retail data analytics platform processing millions of daily transactions, high-frequency seller score changes during flash sales, sub-millisecond timestamp order lookups, and massive user-item recommendation matrices. 

This repository implements the core **Divide-and-Conquer Engine** powering KartIQ, addressing four mission-critical analytical modules:
1. **Module 1: Nightly Order Consolidation** — Stable Merge Sort to consolidate 10,000,000 multi-gateway order records preserving original arrival timestamps.
2. **Module 2: Live Seller Leaderboard** — Randomized-Pivot Quick Sort to reorder 100,000 seller scores during flash sales without falling into worst-case quadratic degradation.
3. **Module 3: High-Frequency Order Lookup** — Binary Search (First Occurrence / Lower-Bound) to locate the earliest order matching a target timestamp in $O(\log n)$ time.
4. **Module 4: Recommendation Scoring Engine** — Hybrid Strassen's Matrix Multiplication to multiply $1024 \times 1024$ user-item matrices with sub-cubic complexity.

---

## 2. Repository Structure

```text
CO3_AT3/
│
├── Module_1_Merge_Sort/
│   ├── Pseudocode/
│   │   └── merge_sort.txt
│   ├── Source_Code/
│   │   └── merge_sort.py
│   └── Report/
│       └── Module_1_Merge_Sort_Report.md
│
├── Module_2_Quick_Sort/
│   ├── Pseudocode/
│   │   └── quick_sort.txt
│   ├── Source_Code/
│   │   └── quick_sort.py
│   └── Report/
│       └── Module_2_Quick_Sort_Report.md
│
├── Module_3_Binary_Search/
│   ├── Pseudocode/
│   │   └── binary_search_first.txt
│   ├── Source_Code/
│   │   └── binary_search_first.py
│   └── Report/
│       └── Module_3_Binary_Search_Report.md
│
├── Module_4_Strassen_Matrix_Multiplication/
│   ├── Pseudocode/
│   │   └── strassen.txt
│   ├── Source_Code/
│   │   └── strassen.py
│   └── Report/
│       └── Module_4_Strassen_Report.md
│
├── Final_Design_and_Analysis/
│   ├── CO3_AT3_Case_Study_Report.pdf
│   └── Final_Design_and_Analysis.md
│
├── Supporting_Files/
│   ├── datasets/
│   │   ├── matrices.json
│   │   ├── orders.json
│   │   └── seller_scores.json
│   ├── results/
│   │   └── test_output.txt
│   ├── screenshots/
│   │   └── README.txt
│   ├── run_experiments.py
│   └── test_all.py
│
├── .gitignore
└── README.md
```

---

## 3. Algorithmic Specifications & Complexities

| Module | Algorithm | Time Complexity (Best / Avg / Worst) | Auxiliary Space | Recurrence Relation |
| :--- | :--- | :--- | :--- | :--- |
| **Module 1** | Stable Merge Sort | $\Theta(n \log n) / \Theta(n \log n) / \Theta(n \log n)$ | $\Theta(n)$ | $T(n) = 2T(n/2) + \Theta(n)$ |
| **Module 2** | Randomized Quick Sort | $\Theta(n \log n) / \Theta(n \log n) / \Theta(n^2)$ | $O(\log n)$ stack | $T(n) = 2T(n/2) + \Theta(n)$ (avg) |
| **Module 3** | Binary Search (First Occur) | $\Theta(1) / \Theta(\log n) / \Theta(\log n)$ | $\Theta(1)$ | $T(n) = T(n/2) + \Theta(1)$ |
| **Module 4** | Hybrid Strassen's Matrix Mult | $\Theta(n^{\log_2 7}) \approx \Theta(n^{2.807})$ | $\Theta(n^2)$ | $T(n) = 7T(n/2) + \Theta(n^2)$ |

### Production Workload Calculations
- **Module 1 (10,000,000 Orders)**:
  - Estimated operations: $n \log_2 n \approx 10^7 \times 23.2535 \approx 2.325 \times 10^8$ operations.
  - Memory: $10^7 \times 64 \text{ bytes} \approx 640\text{ MB} + 640\text{ MB buffer} \approx 1.28\text{ GB RAM}$.
- **Module 2 (100,000 Sellers)**:
  - Deterministic pivot on nearly-sorted data: $\approx \frac{n(n-1)}{2} \approx 4,999,950,000$ comparisons ($O(n^2)$).
  - Randomized pivot expected comparisons: $\approx 1,660,964$ ($>3000\times$ faster).
- **Module 3 (10,000,000 Orders Lookup)**:
  - Search decision depth: $\lceil \log_2(10^7 + 1) \rceil = 24$ comparisons maximum (vs $5 \times 10^6$ for linear scan).
- **Module 4 (1024 × 1024 Recommendation Matrix)**:
  - Conventional scalar multiplications: $1024^3 = 1,073,741,824$.
  - Strassen scalar multiplications: $7^{\log_2 1024} = 7^{10} = 282,475,249$ ($\approx 3.801\times$ fewer multiplications).

---

## 4. Prerequisites & Installation

### Requirements
- Python 3.10 or higher.
- Standard Python libraries only (`sys`, `os`, `json`, `time`, `random`, `typing`). No third-party dependencies required.

### Setup
Clone the repository:
```bash
git clone https://github.com/visshaalpvt/CO3-Assessment-Tool-3-Case-Study-Divide-and-Conquer-Engine-of-a-Retail-Data-Analytics-Platform.git
cd CO3-Assessment-Tool-3-Case-Study-Divide-and-Conquer-Engine-of-a-Retail-Data-Analytics-Platform
```

---

## 5. Execution Instructions

### Running Individual Modules
Execute each algorithm with sample inputs:
```bash
# Module 1: Merge Sort
python Module_1_Merge_Sort/Source_Code/merge_sort.py

# Module 2: Quick Sort
python Module_2_Quick_Sort/Source_Code/quick_sort.py

# Module 3: Binary Search (First Occurrence)
python Module_3_Binary_Search/Source_Code/binary_search_first.py

# Module 4: Strassen's Matrix Multiplication
python Module_4_Strassen_Matrix_Multiplication/Source_Code/strassen.py
```
*(On Windows systems where `python` maps to the Python launcher, use `py` instead of `python`)*.

### Running Test Harness
Validate all 4 modules simultaneously:
```bash
python Supporting_Files/test_all.py
```

### Running Performance Experiments
Benchmark scaling behavior across dataset sizes ($n = 1000, 2000, 4000, 8000$):
```bash
python Supporting_Files/run_experiments.py
```

---

## 6. Testing Status (Actual Execution Results)

All tests have been executed and verified in the target environment:

```text
PASS: stable merge sort
PASS: randomized quick sort
PASS: first-occurrence binary search
PASS: Strassen agrees with conventional multiplication
All 4 module test groups passed.
```

### Verified Benchmark Output (`run_experiments.py`):
```text
experiment,n,seconds,verified
merge_sort,1000,0.003254,True
quick_sort,1000,0.002441,True
merge_sort,2000,0.006691,True
quick_sort,2000,0.004542,True
merge_sort,4000,0.014721,True
quick_sort,4000,0.010600,True
merge_sort,8000,0.033009,True
quick_sort,8000,0.028353,True
```

---

## 7. Key Design Decisions, Limitations & Recommendations

1. **Stability In Merge Sort**:
   - Merge condition `L[i][0] <= R[j][0]` prioritizes the left subarray upon key collisions, ensuring deterministic transaction ordering.
   - *Recommendation*: For datasets exceeding system RAM ($> 10^7$ rows), employ multi-way External Merge Sort with intermediate chunks spilled to NVMe SSDs.
2. **Pivot Selection In Quick Sort**:
   - Uniform random pivot selection mitigates worst-case inputs ($O(n^2)$) caused by nearly-sorted flash sale scores.
   - *Recommendation*: Production systems should deploy Introsort, falling back to Heapsort if recursion depth exceeds $2 \lfloor \log_2 n \rfloor$.
3. **Lower-Bound Binary Search**:
   - When a timestamp match is encountered, the algorithm records the candidate index and shifts $high = mid - 1$, guaranteeing retrieval of the earliest order.
4. **Hybrid Strassen Cutoff**:
   - Strassen's method introduces matrix allocation overhead and extra additions. A hybrid cutoff ($n \le 64$) switches to standard matrix multiplication to preserve cache locality and SIMD throughput.
