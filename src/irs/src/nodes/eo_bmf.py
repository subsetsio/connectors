"""IRS Exempt Organizations Business Master File (eo-bmf).

One CSV per US state / territory / region, probed at eo_<state>.csv.
"""

from __future__ import annotations

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec

from utils import (
    BASE,
    _csv_dicts,
    _fetch,
    _int,
    _str,
    _write_batch,
)

# US states + DC + Puerto Rico + international, for the EO BMF per-state files.
_BMF_STATES = [
    "al", "ak", "az", "ar", "ca", "co", "ct", "de", "fl", "ga", "hi", "id",
    "il", "in", "ia", "ks", "ky", "la", "me", "md", "ma", "mi", "mn", "ms",
    "mo", "mt", "ne", "nv", "nh", "nj", "nm", "ny", "nc", "nd", "oh", "ok",
    "or", "pa", "ri", "sc", "sd", "tn", "tx", "ut", "vt", "va", "wa", "wv",
    "wi", "wy", "dc", "pr", "xx",
]

_BMF_STR_COLS = [
    "ein", "name", "ico", "street", "city", "state", "zip", "group",
    "subsection", "affiliation", "classification", "ruling", "deductibility",
    "foundation", "activity", "organization", "status", "tax_period",
    "asset_cd", "income_cd", "filing_req_cd", "pf_filing_req_cd", "acct_pd",
    "ntee_cd", "sort_name",
]
_BMF_NUM_COLS = ["asset_amt", "income_amt", "revenue_amt"]


def _bmf_schema() -> pa.Schema:
    fields = [(c, pa.string()) for c in _BMF_STR_COLS]
    fields += [(c, pa.int64()) for c in _BMF_NUM_COLS]
    return pa.schema(fields)


def fetch_bmf(node_id: str) -> None:
    asset = node_id
    schema = _bmf_schema()

    def to_rows(content: bytes):
        for r in _csv_dicts(content):
            row = {c: _str(r.get(c)) for c in _BMF_STR_COLS}
            for c in _BMF_NUM_COLS:
                row[c] = _int(r.get(c))
            yield row

    found = 0
    for st in _BMF_STATES:
        content = _fetch(f"{BASE}/eo_{st}.csv")
        if content is None:
            continue
        _write_batch(f"{asset}-{st}", schema, to_rows(content))
        found += 1
    if not found:
        raise RuntimeError(f"{asset}: discovered no EO BMF state files under {BASE}")


DOWNLOAD_SPECS = [
    NodeSpec(id="irs-eo-bmf", fn=fetch_bmf, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(id=f"{s.id}-transform", deps=[s.id], sql=f'SELECT * FROM "{s.id}"')
    for s in DOWNLOAD_SPECS
]
