import sys, random, time, json, csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.extend([
 str(ROOT/"Module_1_Merge_Sort/Source_Code"),
 str(ROOT/"Module_2_Quick_Sort/Source_Code"),
 str(ROOT/"Module_4_Strassen_Matrix_Multiplication/Source_Code")])
from merge_sort import merge_sort_orders
from quick_sort import quick_sort
from strassen import strassen_multiply, conventional_multiply

rng=random.Random(2026)
rows=[]
for n in (1000, 2000, 4000, 8000):
    data=[(rng.randrange(0, n//3+1), f"O{i}") for i in range(n)]
    start=time.perf_counter(); result=merge_sort_orders(data); elapsed=time.perf_counter()-start
    assert result == sorted(data, key=lambda x:x[0])  # stable Python reference sort
    rows.append({"experiment":"merge_sort","n":n,"seconds":round(elapsed,6),"verified":True})
    scores=[rng.randrange(0,n) for _ in range(n)]
    start=time.perf_counter(); qs=quick_sort(scores.copy(),seed=2026); qtime=time.perf_counter()-start
    assert qs==sorted(scores)
    rows.append({"experiment":"quick_sort","n":n,"seconds":round(qtime,6),"verified":True})
out=ROOT/"Supporting_Files/results/experiment_results.csv"
with out.open("w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=["experiment","n","seconds","verified"]); w.writeheader(); w.writerows(rows)
print(out.read_text())
print("Timings are environment-dependent; rerun locally for your machine's measurements.")
