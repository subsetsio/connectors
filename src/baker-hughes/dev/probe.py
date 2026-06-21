"""Probe: exercise discovery + every parse path against the live site.
Does NOT call save_raw_* — just reports shapes so we can author tests from reality.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import nodes.baker_hughes as bh


def summarize(name, rows):
    print(f"\n=== {name}: {len(rows)} rows ===")
    if not rows:
        print("  (EMPTY)")
        return
    keys = rows[0].keys()
    print("  cols:", list(keys))
    print("  first:", rows[0])
    print("  last :", rows[-1])
    # date / year ranges
    for k in ("year", "month"):
        vals = [r[k] for r in rows if r.get(k) is not None]
        if vals:
            print(f"  {k}: min={min(vals)} max={max(vals)}")
    for k in ("date", "publish_date"):
        vals = [r[k] for r in rows if r.get(k) is not None]
        if vals:
            print(f"  {k}: min={min(vals)} max={max(vals)} (nonnull {len(vals)}/{len(rows)})")
    cnts = [r["rig_count"] for r in rows if r.get("rig_count") is not None]
    if cnts:
        print(f"  rig_count: min={min(cnts)} max={max(cnts)} n={len(cnts)}")


bh.configure_http(headers={"User-Agent": bh._UA})

na_files = bh._discover(bh.NA_PAGE)
print("NA page files:")
for u, fn in na_files:
    print(" ", u, "|", fn)

na_uuid = bh._pick_na_current(na_files)
print("picked NA current:", na_uuid)
content = bh._download(na_uuid)
summarize("NAM Weekly", bh._parse_na_long(content, "NAM Weekly", weekly=True))
summarize("NAM Monthly", bh._parse_na_long(content, "NAM Monthly", weekly=False))

state_uuid = bh._pick_match(na_files, "rigs by state")
summarize("State historical", bh._parse_state_hist(bh._download(state_uuid)))

intl_files = bh._discover(bh.INTL_PAGE)
print("\nINTL page files:")
for u, fn in intl_files:
    print(" ", u, "|", fn)

ww_uuid = bh._pick_ww_current(intl_files)
print("picked WW current:", ww_uuid)
summarize("WW Monthly", bh._parse_ww_long(bh._download(ww_uuid)))

wwh_uuid = bh._pick_match(intl_files, "worldwide rig count", "2007")
summarize("WW historical", bh._parse_ww_hist(bh._download(wwh_uuid)))
