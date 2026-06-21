from subsets_utils import get
r = get("https://berkeley-earth-temperature.s3.us-west-1.amazonaws.com/Global/Land_and_Ocean_complete.txt", timeout=(10,120))
lines = r.text.splitlines()
# find all data-section header lines and count data lines between them
import re
data_idx = [i for i,l in enumerate(lines) if l.strip() and not l.lstrip().startswith('%') and len(l.split())==12 and l.split()[0].isdigit()]
print("total 12-col data lines:", len(data_idx))
# find gaps (section breaks) where index jumps
breaks=[data_idx[0]]
for a,b in zip(data_idx, data_idx[1:]):
    if b-a>1: breaks.append(b)
print("num contiguous sections:", len(breaks), "starts:", breaks[:5])
# print the comment lines just before the 2nd section
if len(breaks)>1:
    s2=breaks[1]
    print("--- context before 2nd data section (line", s2, ") ---")
    for l in lines[s2-14:s2]:
        print(repr(l[:140]))
