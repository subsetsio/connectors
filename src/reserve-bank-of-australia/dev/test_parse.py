import sys
sys.path.insert(0, "src")
from nodes.reserve_bank_of_australia import _fetch_csv_text, _parse_rba_csv, configure_http, _USER_AGENT

configure_http(headers={"User-Agent": _USER_AGENT})

for slug, pk in [("g1-data",None),("a2-data",None),("a3-daily-open-market-operations",None),
                 ("j1-cash-rate","cash-rate"),("b12.1.1-africa-and-middle-east","africa-and-middle-east"),
                 ("f11.1-data",None),("h5-data",None),("c2.2-by-card-type",None)]:
    text=_fetch_csv_text(slug)
    rows=_parse_rba_csv(text, slug, pk)
    print(f"{slug}: {len(rows)} long rows")
    if rows:
        r=rows[0]
        print("   first:", {k:r[k] for k in ('series_id','obs_date','value_text','units','frequency','partition_key')})
        # distinct series
        sids={r['series_id'] for r in rows}
        print("   distinct series:", len(sids), "sample dates:", sorted({r['obs_date'] for r in rows})[:1], "->", sorted({r['obs_date'] for r in rows})[-1:])
