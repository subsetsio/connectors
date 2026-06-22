"""Exercise the real parse helpers + transform SQL on a small slice."""
import sys
sys.path.insert(0, "src")
import duckdb
import importlib.util

spec = importlib.util.spec_from_file_location("bom", "src/nodes/box_office_mojo.py")
bom = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bom)

BASE = bom.BASE


def slice_rows(url, colmap, extra=None):
    df = bom._read_table(bom._get_html(url))
    return bom._str_rows(df, colmap, extra)


def run(name, rows, sql_template):
    con = duckdb.connect()
    con.register(name, __import__("pyarrow").Table.from_pylist(rows))
    sql = sql_template.replace(f'"{name}"', name)
    out = con.execute(sql).arrow()
    print("=" * 60)
    print(name, "-> rows:", out.num_rows)
    print("schema:", [(f.name, str(f.type)) for f in out.schema])
    print(out.slice(0, 3).to_pydict())


# pick one transform per entity, feed a one-page slice
cases = {
    "box-office-mojo-yearly-summary": (
        slice_rows(f"{BASE}/year/", bom.YEARLY_SUMMARY_COLS),),
    "box-office-mojo-domestic-yearly": (
        slice_rows(f"{BASE}/year/2023/", bom.DOMESTIC_YEARLY_COLS, {"year": "2023"}),),
    "box-office-mojo-worldwide-yearly": (
        slice_rows(f"{BASE}/year/world/2023/", bom.WORLDWIDE_YEARLY_COLS, {"year": "2023"}),),
    "box-office-mojo-weekend-summary": (
        slice_rows(f"{BASE}/weekend/?yr=2023", bom.WEEKEND_SUMMARY_COLS, {"year": "2023"}),),
    "box-office-mojo-domestic-weekend": (
        slice_rows(f"{BASE}/weekend/2023W26/", bom.WEEKEND_DETAIL_COLS,
                   {"weekend_id": "2023W26", "year": "2023", "week": "26"}),),
    "box-office-mojo-domestic-daily": (
        slice_rows(f"{BASE}/daily/2023/", bom.DAILY_COLS, {"year": "2023"}),),
    "box-office-mojo-top-lifetime-grosses": (
        slice_rows(f"{BASE}/chart/top_lifetime_gross/", bom.TOP_LIFETIME_COLS),),
}

by_dep = {s.deps[0]: s.sql for s in bom.TRANSFORM_SPECS}
for name, (rows,) in cases.items():
    run(name, rows, by_dep[name])
