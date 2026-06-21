import sys
sys.path.insert(0, "src")
from nodes.nber import _parse_dat, _parse_doc, _get
for ch, stem in [("01","a01005a"),("01","m01001"),("01","q01112")]:
    txt = _get(f"https://data.nber.org/databases/macrohistory/rectdata/{ch}/{stem}.dat").text
    rows = _parse_dat(stem, ch, txt)
    print(stem, "rows", len(rows), "sample", rows[:2], rows[-1:])
txt = _get("https://data.nber.org/databases/macrohistory/rectdata/01/docs/a01005a.txt").text
print("doc", _parse_doc(txt))
