from subsets_utils import get
import re
# Full dataflow listing
r = get("https://api.statistiken.bundesbank.de/rest/metadata/dataflow/BBK", timeout=(15,120))
txt = r.text
ids = set(re.findall(r'Dataflow=BBK:([A-Z0-9]+)\(', txt)) | set(re.findall(r'id="([A-Z0-9]+)"', txt))
for f in ["BBBK13","BBBK20","BBBP2","BBDG1","BBXP1","BBKRT","BBDA1"]:
    print(f, "in_list:", f in ids)
print("total ids in dataflow list:", len(ids))

# BBKRT datastructure dimensions
print("\n=== BBKRT structure (find dimensions) ===")
r2 = get("https://api.statistiken.bundesbank.de/rest/metadata/datastructure/BBK/BBK_KRT?references=children", timeout=(15,120))
print("ds status (BBK_KRT guess):", r2.status_code)
