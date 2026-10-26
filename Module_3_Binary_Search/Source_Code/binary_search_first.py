from typing import List, Tuple

Order = Tuple[int, str]

def binary_search_first_timestamp(orders: List[Order], target: int) -> int:
    """Return index of first order with target timestamp, or -1 if absent.
    Precondition: orders are sorted by timestamp in nondecreasing order.
    """
    low, high, answer = 0, len(orders) - 1, -1
    while low <= high:
        mid = low + (high - low) // 2
        if orders[mid][0] >= target:
            if orders[mid][0] == target:
                answer = mid
            high = mid - 1
        else:
            low = mid + 1
    return answer

if __name__ == "__main__":
    orders = [(101,"O4"),(102,"O2"),(102,"O5"),(103,"O6"),(105,"O1"),(105,"O3")]
    for t in (102, 104, 105):
        i = binary_search_first_timestamp(orders, t)
        print(t, "->", i, orders[i] if i != -1 else "not found")
