import sys; sys.path.insert(0, 'src')
import nodes.cbn as c
c.DATE_FLOOR_YEAR = 2013   # speed: skip empty 1960-2012 years for this test
tid = 48
info = c._indicators_for_table(tid); ids = [i for i, _ in info]; names = [n for _, n in info]
out = {}
found = c._fetch_daily(tid, ids, names, 2025, out)
rows = list(out.values())
print("found", found, "rows", len(rows))
ds = [r['date'] for r in rows]
print("date range", min(ds), max(ds))
import collections
ym = collections.Counter(r['date'].strftime('%Y') for r in rows)
print("rows per year:", dict(sorted(ym.items())))
print("distinct indicator_ids", len(set(r['indicator_id'] for r in rows)), "of", len(ids))
s = sorted([r for r in rows if r['indicator_id'] == ids[0]], key=lambda x: x['date'])
print("ind0", names[0])
for r in s[-3:]: print("  ", r['period'], r['date'], r['value'])
