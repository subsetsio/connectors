from subsets_utils import get

BASE = "https://data.weather.gov.hk/weatherAPI/opendata/opendata.php"


def show(label, **params):
    params.setdefault("rformat", "csv")
    r = get(BASE, params=params, timeout=(10.0, 120.0))
    body = r.text
    print(f"\n===== {label} :: {params} :: status={r.status_code} len={len(body)} =====")
    lines = body.splitlines()
    for ln in lines[:8]:
        print(repr(ln))
    print(f"... total lines={len(lines)}; last:")
    for ln in lines[-3:]:
        print(repr(ln))


# CLMTEMP without year (full history) -- HKO
show("CLMTEMP HKO no-year", dataType="CLMTEMP", station="HKO")
# tides hourly without year
show("HHOT CCH no-year", dataType="HHOT", station="CCH")
# tides hourly with current-ish years
for y in (2024, 2025, 2026, 2027):
    show(f"HHOT CCH {y}", dataType="HHOT", station="CCH", year=y)
# high/low tides
show("HLT CCH 2026", dataType="HLT", station="CCH", year=2026)
# sun times no-year and with year
show("SRS no-year", dataType="SRS")
show("SRS 2026", dataType="SRS", year=2026)
# moon times
show("MRS no-year", dataType="MRS")
show("MRS 2026", dataType="MRS", year=2026)
