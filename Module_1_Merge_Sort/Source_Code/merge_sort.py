from typing import List, Tuple

Order = Tuple[int, str]  # (timestamp, order ID)

def merge_sort_orders(orders: List[Order]) -> List[Order]:
    """Stable merge sort by timestamp; input is not mutated."""
    if len(orders) <= 1:
        return list(orders)
    mid = len(orders) // 2
    left = merge_sort_orders(orders[:mid])
    right = merge_sort_orders(orders[mid:])
    return _merge(left, right)

def _merge(left: List[Order], right: List[Order]) -> List[Order]:
    result, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        # <= selects the left item on ties, preserving original arrival order.
        if left[i][0] <= right[j][0]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

if __name__ == "__main__":
    sample = [(105, "O1"), (102, "O2"), (105, "O3"),
              (101, "O4"), (102, "O5"), (103, "O6")]
    print("Input:", sample)
    print("Sorted:", merge_sort_orders(sample))
