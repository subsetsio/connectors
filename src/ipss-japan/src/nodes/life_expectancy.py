"""JMD period life expectancy at birth (jmd-life-expectancy).

E0per.txt: 'Year Female Male Total' — period life expectancy at birth. No Age
column; area is a *column*.
"""

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import _data_lines, _iter_areas, _num, _year


def fetch_life_expectancy(node_id: str) -> None:
    """E0per.txt: 'Year Female Male Total' — period life expectancy at birth.
    No Age column."""
    cols = {k: [] for k in ("area", "area_name", "year", "female", "male", "total")}
    for code, name, text in _iter_areas("E0per.txt"):
        for line in _data_lines(text):
            tok = line.split()
            if len(tok) < 4:
                continue
            yr = _year(tok[0])
            if yr is None:
                continue
            cols["area"].append(code)
            cols["area_name"].append(name)
            cols["year"].append(yr)
            cols["female"].append(_num(tok[1]))
            cols["male"].append(_num(tok[2]))
            cols["total"].append(_num(tok[3]))
    schema = pa.schema([
        ("area", pa.string()), ("area_name", pa.string()),
        ("year", pa.int32()),
        ("female", pa.float64()), ("male", pa.float64()), ("total", pa.float64()),
    ])
    table = pa.table({k: cols[k] for k in schema.names}, schema=schema)
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="ipss-japan-jmd-life-expectancy",
        fn=fetch_life_expectancy,
        kind="download",
    ),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="ipss-japan-jmd-life-expectancy-transform",
        deps=["ipss-japan-jmd-life-expectancy"],
        sql='''
            SELECT area, area_name, CAST(year AS INTEGER) AS year,
                   female, male, total
            FROM "ipss-japan-jmd-life-expectancy"
            WHERE year IS NOT NULL
        ''',
    ),
]
