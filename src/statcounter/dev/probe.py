import csv, io, re
from subsets_utils import get

def fetch(params):
    r = get("https://gs.statcounter.com/chart.php", params=params, timeout=(10.0, 120.0))
    r.raise_for_status()
    return r.content.decode("utf-8-sig", errors="replace")

# timeseries: browser, worldwide, full history
txt = fetch({
    "statType_hidden": "browser", "region_hidden": "ww", "granularity": "monthly",
    "csv": "1", "device_hidden": "desktop+tablet+mobile", "multi-device": "true",
    "fromMonthYear": "2009-01", "toMonthYear": "2026-06",
})
rows = list(csv.reader(io.StringIO(txt)))
print("browser ww: header[:4]=", rows[0][:4], "ncols=", len(rows[0]), "nrows=", len(rows)-1)
print("  first data:", rows[1][:3], "last:", rows[-1][:3])
print("  date regex first:", bool(re.match(r'^\d{4}-\d{2}$', rows[1][0])))

# a tiny country to see what a sparse region returns
txt2 = fetch({
    "statType_hidden": "social_media", "region_hidden": "TV", "granularity": "monthly",
    "csv": "1", "device_hidden": "desktop+tablet+mobile", "multi-device": "true",
    "fromMonthYear": "2009-01", "toMonthYear": "2026-06",
})
rows2 = list(csv.reader(io.StringIO(txt2)))
print("social TV: header[0]=", rows2[0][0] if rows2 else None, "ncols=", len(rows2[0]) if rows2 else 0, "nrows=", len(rows2)-1)

# resolution yearly
txt3 = fetch({
    "statType_hidden": "resolution", "region_hidden": "ww", "granularity": "yearly",
    "csv": "1", "device_hidden": "desktop+tablet+mobile", "multi-device": "true",
    "fromYear": "2015", "toYear": "2015",
})
rows3 = list(csv.reader(io.StringIO(txt3)))
print("resolution ww 2015: header=", rows3[0], "rows=", rows3[1:4])
