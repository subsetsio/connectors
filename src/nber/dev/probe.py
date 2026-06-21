from subsets_utils import get
def show(url, n=25):
    print("="*70)
    print(url)
    r = get(url, timeout=(10,60))
    print("status", r.status_code, "len", len(r.text))
    print("-"*40)
    print("\n".join(r.text.splitlines()[:n]))
# annual
show("https://data.nber.org/databases/macrohistory/rectdata/01/a01005a.dat", 8)
# monthly
show("https://data.nber.org/databases/macrohistory/rectdata/01/m01001.dat", 10)
# quarterly
show("https://data.nber.org/databases/macrohistory/rectdata/01/q01112.dat", 10)
# docs txt for annual
show("https://data.nber.org/databases/macrohistory/rectdata/01/docs/a01005a.txt", 40)
