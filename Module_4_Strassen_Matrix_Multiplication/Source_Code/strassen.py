from typing import List

Matrix = List[List[int]]

def conventional_multiply(A: Matrix, B: Matrix) -> Matrix:
    n = len(A)
    if n == 0 or any(len(row) != n for row in A + B) or len(B) != n:
        raise ValueError("Matrices must be non-empty square matrices of equal size")
    return [[sum(A[i][k] * B[k][j] for k in range(n))
             for j in range(n)] for i in range(n)]

def _add(A, B):
    n = len(A)
    return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]

def _sub(A, B):
    n = len(A)
    return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]

def _split(A):
    n = len(A); h = n // 2
    return ([row[:h] for row in A[:h]], [row[h:] for row in A[:h]],
            [row[:h] for row in A[h:]], [row[h:] for row in A[h:]])

def _join(C11, C12, C21, C22):
    return [C11[i] + C12[i] for i in range(len(C11))] + \
           [C21[i] + C22[i] for i in range(len(C21))]

def strassen_multiply(A: Matrix, B: Matrix, cutoff: int = 32) -> Matrix:
    """Strassen multiplication with padding to a power of two and a hybrid cutoff."""
    if not A or not B or len(A) != len(B):
        raise ValueError("Matrices must be non-empty and have equal dimensions")
    n = len(A)
    if any(len(r) != n for r in A) or any(len(r) != n for r in B):
        raise ValueError("Matrices must be square")
    size = 1
    while size < n: size *= 2
    Ap = [row[:] + [0] * (size - n) for row in A] + [[0] * size for _ in range(size - n)]
    Bp = [row[:] + [0] * (size - n) for row in B] + [[0] * size for _ in range(size - n)]
    def rec(X, Y):
        m = len(X)
        if m <= cutoff or m == 1:
            return conventional_multiply(X, Y)
        A11, A12, A21, A22 = _split(X)
        B11, B12, B21, B22 = _split(Y)
        M1 = rec(_add(A11, A22), _add(B11, B22))
        M2 = rec(_add(A21, A22), B11)
        M3 = rec(A11, _sub(B12, B22))
        M4 = rec(A22, _sub(B21, B11))
        M5 = rec(_add(A11, A12), B22)
        M6 = rec(_sub(A21, A11), _add(B11, B12))
        M7 = rec(_sub(A12, A22), _add(B21, B22))
        C11 = _add(_sub(_add(M1, M4), M5), M7)
        C12 = _add(M3, M5)
        C21 = _add(M2, M4)
        C22 = _add(_sub(_add(M1, M3), M2), M6)
        return _join(C11, C12, C21, C22)
    Cp = rec(Ap, Bp)
    return [row[:n] for row in Cp[:n]]

if __name__ == "__main__":
    A = [[1, 7], [3, 5]]
    B = [[1, 3], [7, 5]]
    print("Strassen:", strassen_multiply(A, B, cutoff=1))
    print("Conventional:", conventional_multiply(A, B))
