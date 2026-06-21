"""JMD period life tables (jmd-life-tables).

fltper/mltper/bltper 1x1 (Female/Male/Total). Columns Year Age mx qx ax lx dx
Lx Tx ex; sex is folded into a *column*, so this fetcher loops over the three
per-sex files. DuckDB folds identifiers case-insensitively, so lx/Lx would
collide — Lx/Tx are renamed to distinct names.
"""

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import _data_lines, _iter_areas, _num, _year

# File column order is: mx qx ax lx dx Lx Tx ex.
_LT_VALUE_COLS = [
    "mx", "qx", "ax", "lx", "dx", "person_years", "total_person_years", "ex",
]


def fetch_life_tables(node_id: str) -> None:
    """Period life tables: fltper/mltper/bltper (Female/Male/Total) at 1x1.
    Columns Year Age mx qx ax lx dx Lx Tx ex; sex folded into a column."""
    sex_files = {
        "Female": "fltper_1x1.txt",
        "Male": "mltper_1x1.txt",
        "Total": "bltper_1x1.txt",
    }
    cols = {k: [] for k in
            ("area", "area_name", "sex", "year", "age", *_LT_VALUE_COLS)}
    ncols = 2 + len(_LT_VALUE_COLS)
    for sex, filename in sex_files.items():
        for code, name, text in _iter_areas(filename):
            for line in _data_lines(text):
                tok = line.split()
                if len(tok) < ncols:
                    continue
                yr = _year(tok[0])
                if yr is None:
                    continue
                cols["area"].append(code)
                cols["area_name"].append(name)
                cols["sex"].append(sex)
                cols["year"].append(yr)
                cols["age"].append(tok[1])
                for i, vc in enumerate(_LT_VALUE_COLS):
                    cols[vc].append(_num(tok[2 + i]))

    schema = pa.schema(
        [("area", pa.string()), ("area_name", pa.string()),
         ("sex", pa.string()), ("year", pa.int32()), ("age", pa.string())]
        + [(vc, pa.float64()) for vc in _LT_VALUE_COLS]
    )
    table = pa.table({k: cols[k] for k in schema.names}, schema=schema)
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="ipss-japan-jmd-life-tables",
        fn=fetch_life_tables,
        kind="download",
    ),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="ipss-japan-jmd-life-tables-transform",
        deps=["ipss-japan-jmd-life-tables"],
        sql='''
            SELECT area, area_name, sex,
                   CAST(year AS INTEGER) AS year, age,
                   mx, qx, ax, lx, dx, person_years, total_person_years, ex
            FROM "ipss-japan-jmd-life-tables"
            WHERE year IS NOT NULL AND age IS NOT NULL
        ''',
    ),
]
