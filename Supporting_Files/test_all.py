import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "Module_1_Merge_Sort/Source_Code"))
sys.path.insert(0, str(ROOT / "Module_2_Quick_Sort/Source_Code"))
sys.path.insert(0, str(ROOT / "Module_3_Binary_Search/Source_Code"))
sys.path.insert(0, str(ROOT / "Module_4_Strassen_Matrix_Multiplication/Source_Code"))
from merge_sort import merge_sort_orders
from quick_sort import quick_sort
from binary_search_first import binary_search_first_timestamp
from strassen import strassen_multiply, conventional_multiply

orders=[(105,"O1"),(102,"O2"),(105,"O3"),(101,"O4"),(102,"O5"),(103,"O6")]
sorted_orders=merge_sort_orders(orders)
assert sorted_orders == [(101,"O4"),(102,"O2"),(102,"O5"),(103,"O6"),(105,"O1"),(105,"O3")]
assert [x[1] for x in sorted_orders if x[0]==102] == ["O2","O5"]
scores=[42,17,63,8,55,29]
assert quick_sort(scores.copy(), seed=7) == sorted(scores)
assert binary_search_first_timestamp(sorted_orders,102)==1
assert binary_search_first_timestamp(sorted_orders,104)==-1
A=[[1,7],[3,5]]; B=[[1,3],[7,5]]
assert strassen_multiply(A,B,cutoff=1)==[[50,38],[38,34]]
assert strassen_multiply(A,B,cutoff=2)==conventional_multiply(A,B)
print("PASS: stable merge sort")
print("PASS: randomized quick sort")
print("PASS: first-occurrence binary search")
print("PASS: Strassen agrees with conventional multiplication")
print("All 4 module test groups passed.")
