"""JMD age-standardized death rates by cause (jmd-age-standardized-death-rates).

ASDR_HI.csv: a real CSV after a 1-line title. Header:
prefecture,sex,list,agef,cause,year,ASDR. Only the HI cause list is published
(JMDC/HCD/Condensed are absent at the source). Area is a *column*.
"""

import csv
import io

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import _iter_areas, _num, _year


def fetch_asdr(node_id: str) -> None:
    """ASDR_HI.csv: a real CSV after a 1-line title.
    Header: prefecture,sex,list,agef,cause,year,ASDR. Only the HI cause list is
    published (JMDC/HCD/Condensed are absent at the source)."""
    cols = {k: [] for k in
            ("area", "area_name", "prefecture", "sex", "list",
             "agef", "cause", "year", "asdr")}
    for code, name, text in _iter_areas("ASDR_HI.csv"):
        # Drop the leading provenance/title line, parse the rest as CSV.
        body = text.split("\n", 1)[1] if "\n" in text else ""
        reader = csv.DictReader(io.StringIO(body))
        for row in reader:
            yr = _year((row.get("year") or "").strip())
            if yr is None:
                continue
            cols["area"].append(code)
            cols["area_name"].append(name)
            cols["prefecture"].append((row.get("prefecture") or "").strip() or None)
            cols["sex"].append((row.get("sex") or "").strip() or None)
            cols["list"].append((row.get("list") or "").strip() or None)
            agef = (row.get("agef") or "").strip()
            cause = (row.get("cause") or "").strip()
            cols["agef"].append(int(agef) if agef.isdigit() else None)
            cols["cause"].append(int(cause) if cause.lstrip("-").isdigit() else None)
            cols["year"].append(yr)
            cols["asdr"].append(_num((row.get("ASDR") or "").strip()))
    schema = pa.schema([
        ("area", pa.string()), ("area_name", pa.string()),
        ("prefecture", pa.string()), ("sex", pa.string()), ("list", pa.string()),
        ("agef", pa.int32()), ("cause", pa.int32()),
        ("year", pa.int32()), ("asdr", pa.float64()),
    ])
    table = pa.table({k: cols[k] for k in schema.names}, schema=schema)
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="ipss-japan-jmd-age-standardized-death-rates",
        fn=fetch_asdr,
        kind="download",
    ),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="ipss-japan-jmd-age-standardized-death-rates-transform",
        deps=["ipss-japan-jmd-age-standardized-death-rates"],
        sql='''
            SELECT area, area_name, prefecture, sex, list AS cause_list,
                   agef, cause, CAST(year AS INTEGER) AS year, asdr
            FROM "ipss-japan-jmd-age-standardized-death-rates"
            WHERE year IS NOT NULL AND asdr IS NOT NULL
        ''',
    ),
]
