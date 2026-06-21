import re
from subsets_utils import get

def parse(js):
    start = js.index("['Date'")
    end = js.index("]", start)
    header = js[start:end]
    entities = [n for n in re.findall(r"'([^']*)'", header) if n != "Date"]
    rows = re.findall(r"\[new Date\((\d+),(\d+),(\d+)\),([^\]]*)\]", js)
    parsed = []
    for y, m, d, rest in rows:
        vals = [float(x) for x in rest.split(",")]
        parsed.append((int(y), int(m), vals))
    return entities, parsed

for dir_, country in [("PYPL","US"), ("ODE","All"), ("DB","GB")]:
    url = f"https://raw.githubusercontent.com/pypl/pypl.github.io/master/{dir_}/{country}.js"
    js = get(url, timeout=(10,120)).text
    ents, rows = parse(js)
    bad = [r for r in rows if len(r[2]) != len(ents)]
    print(f"{dir_}/{country}: {len(ents)} entities, {len(rows)} rows, first={rows[0][0]}-{rows[0][1]+1}, last={rows[-1][0]}-{rows[-1][1]+1}, mismatched_rows={len(bad)}, sum_row0={sum(rows[0][2]):.3f}")
