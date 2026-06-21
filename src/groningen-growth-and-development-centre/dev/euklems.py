import sys; sys.path.insert(0,"src")
from subsets_utils import get
for fid,name in [(357147,"18II_output.csv"),(357150,"18II_capital.csv"),(357149,"18II_labour.csv")]:
    print(f"\n=== {name} ({fid}) ===")
    r=get(f"https://dataverse.nl/api/access/datafile/{fid}", timeout=600, headers={"Range":"bytes=0-1200"})
    lines=r.content.decode("utf-8","replace").splitlines()[:4]
    for ln in lines: print("   ", ln[:260])
