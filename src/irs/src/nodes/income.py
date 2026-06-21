"""IRS SOI county-income / zipcode-income tables.

Bulk CSVs probed at <yy>incyallagi.csv (county) / <yy>zpallagi.csv (ZIP). One
parametric fetch drives both subsets — they share the probe loop, parse, and
core SOI variable set, differing only in the geographic key columns.
"""

from __future__ import annotations

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec

from utils import (
    BASE,
    _csv_dicts,
    _fetch,
    _int,
    _num,
    _str,
    _two_digit_years,
    _write_batch,
)

# Curated, well-documented core SOI variables shared by the county/ZIP income
# tables. Counts (number of returns with the item) are integers; amounts (in
# thousands of dollars) are doubles. Columns absent in a given tax year map to
# null — the schema is the contract, not the source's column drift.
_INC_COUNT_CODES = [
    "n1", "n2", "n02650", "n00200", "n00300", "n00600", "n00900", "n01000",
    "n02500", "n04470", "n04800", "n05800", "n07100", "n06500", "n10300",
]
_INC_AMOUNT_CODES = [
    "a00100", "a02650", "a00200", "a00300", "a00600", "a00900", "a01000",
    "a02500", "a04470", "a04800", "a05800", "a07100", "a06500", "a10300",
    "a11901", "a11902",
]


def _income_schema(node_id: str) -> pa.Schema:
    fields = [
        ("tax_year", pa.int32()),
        ("statefips", pa.string()),
        ("state", pa.string()),
    ]
    if node_id == "irs-county-income":
        fields += [("countyfips", pa.string()), ("countyname", pa.string())]
    else:  # irs-zipcode-income
        fields += [("zipcode", pa.string())]
    fields.append(("agi_stub", pa.int32()))
    fields += [(c, pa.int64()) for c in _INC_COUNT_CODES]
    fields += [(c, pa.float64()) for c in _INC_AMOUNT_CODES]
    return pa.schema(fields)


def fetch_income(node_id: str) -> None:
    asset = node_id
    is_county = node_id == "irs-county-income"
    infix = "incy" if is_county else "zp"
    schema = _income_schema(node_id)

    def to_rows(content: bytes, year: int):
        for r in _csv_dicts(content):
            row = {
                "tax_year": year,
                "statefips": _str(r.get("statefips")),
                "state": _str(r.get("state")),
                "agi_stub": _int(r.get("agi_stub")),
            }
            if is_county:
                row["countyfips"] = _str(r.get("countyfips"))
                row["countyname"] = _str(r.get("countyname"))
            else:
                row["zipcode"] = _str(r.get("zipcode"))
            for c in _INC_COUNT_CODES:
                row[c] = _int(r.get(c))
            for c in _INC_AMOUNT_CODES:
                row[c] = _num(r.get(c))
            yield row

    found = 0
    for year in _two_digit_years(2000):
        yy = f"{year % 100:02d}"
        content = _fetch(f"{BASE}/{yy}{infix}allagi.csv")
        if content is None:
            continue
        _write_batch(f"{asset}-{year}", schema, to_rows(content, year))
        found += 1
    if not found:
        raise RuntimeError(f"{asset}: discovered no income files under {BASE}")


DOWNLOAD_SPECS = [
    NodeSpec(id="irs-county-income", fn=fetch_income, kind="download"),
    NodeSpec(id="irs-zipcode-income", fn=fetch_income, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(id=f"{s.id}-transform", deps=[s.id], sql=f'SELECT * FROM "{s.id}"')
    for s in DOWNLOAD_SPECS
]
