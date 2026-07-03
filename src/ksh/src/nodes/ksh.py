"""KSH (Hungarian Central Statistical Office) — High-Value Datasets API.

Mechanism `hvd_api` (https://data.ksh.hu/): a catalog of statistical datasets,
each exposing one or more SDMX *distributions* (resources). Every distribution
is a distinct SDMX dataflow with its own dimension/measure column list, so the
publishable unit is the distribution, keyed by its resource UUID. Data is served
per resource at /datasets/{dataset_id}/data/{resource_id}.{format} in one of two
formats (recorded per resource in src/constants.py):

  - csv  — semicolon-delimited, sometimes quoted; two layouts appear in the wild
           (compact `FREQ;...;TIME;VALUES` and SDMX-CSV `DATAFLOW;REF_AREA;...`).
  - xml  — SDMX-ML 2.0 CompactData: <Series> elements carry the dimension
           attributes, nested <Obs> elements carry TIME_PERIOD/OBS_VALUE/etc.

Fetch shape: **stateless full re-pull** (shape 1). The whole corpus is ~1.3M
observations / low tens of MB across 38 resources — re-fetch every run and
overwrite. No incremental filter is exposed by the API (full corpus per refresh),
so there is no watermark/cursor; revisions are picked up for free.

Because the 38 dataflows are mutually heterogeneous (no shared value or time
column — e.g. the value lives in VALUES, OBS_VALUE, or PROD_SELL_VAL depending on
the dataflow), each resource is parsed to long-format records with every SDMX
column preserved verbatim as a string and written as NDJSON (the format rubric's
choice for heterogeneous records). The transform is a thin SELECT * that publishes
one Delta table per resource.
"""

import csv
import io
import xml.etree.ElementTree as ET

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    save_raw_ndjson,
)
from constants import ENTITY_META, ENTITY_IDS

BASE = "https://data.ksh.hu"
SLUG = "ksh"


@transient_retry()  # retries transient network errors + 429 + 5xx, then reraises
def _fetch(url):
    resp = get(url, timeout=(10.0, 180.0))
    resp.raise_for_status()  # 4xx (e.g. a withdrawn distribution) propagates -> node fails
    return resp


def _localname(tag):
    return tag.rsplit("}", 1)[-1]


def _clean(value):
    if value is None:
        return None
    value = value.strip()
    return value if value != "" else None


def _parse_csv(text):
    """Semicolon-delimited CSV -> list[dict]. Columns are the header row; empty
    cells become null. Handles both the compact and SDMX-CSV layouts uniformly."""
    reader = csv.reader(io.StringIO(text), delimiter=";")
    rows = list(reader)
    if not rows:
        return []
    header = [h.strip() for h in rows[0]]
    out = []
    for raw in rows[1:]:
        if not any(c.strip() for c in raw):
            continue  # skip blank lines
        record = {}
        for i, col in enumerate(header):
            if not col:
                continue
            record[col] = _clean(raw[i]) if i < len(raw) else None
        out.append(record)
    return out


def _parse_xml(text):
    """SDMX-ML CompactData -> list[dict]. One record per <Obs>, merging its parent
    <Series>'s dimension attributes with the observation's own attributes."""
    root = ET.fromstring(text.encode("utf-8"))
    out = []
    for el in root.iter():
        if _localname(el.tag) != "Series":
            continue
        series_attr = {k: _clean(v) for k, v in el.attrib.items()}
        obs_children = [c for c in el if _localname(c.tag) == "Obs"]
        if obs_children:
            for obs in obs_children:
                record = dict(series_attr)
                for k, v in obs.attrib.items():
                    record[k] = _clean(v)
                out.append(record)
        else:
            # Series with no observations — preserve the dimension key anyway.
            out.append(dict(series_attr))
    return out


def _normalize(rows):
    """Force a uniform key set across every record (missing -> null).

    SDMX-ML Series carry varying attribute sets, so parsed rows within one
    resource can have heterogeneous keys. DuckDB's read_json_auto infers columns
    from a leading sample and errors ("unknown key ...") when a later row carries
    a key the sample never saw. Emitting every row with the full union of keys
    makes the NDJSON objects homogeneous and the schema sample-independent."""
    keys = []
    seen = set()
    for row in rows:
        for k in row:
            if k not in seen:
                seen.add(k)
                keys.append(k)
    return [{k: row.get(k) for k in keys} for row in rows]


def fetch_one(node_id):
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    rid = node_id[len(SLUG) + 1:]  # strip "ksh-" -> resource UUID
    meta = ENTITY_META[rid]
    url = "{}/datasets/{}/data/{}.{}".format(BASE, meta["dataset_id"], rid, meta["format"])
    resp = _fetch(url)
    if meta["format"] == "csv":
        rows = _parse_csv(resp.content.decode("utf-8-sig", errors="replace"))
    else:
        rows = _parse_xml(resp.content.decode("utf-8", errors="replace"))
    save_raw_ndjson(_normalize(rows), asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="{}-{}".format(SLUG, rid), fn=fetch_one, kind="download")
    for rid in ENTITY_IDS
]

# Per-resource observation-period column (temporal). The dataflows split into
# the compact eurostat layout (period column `TIME`) and the SDMX-CSV/XML layout
# (period column `TIME_PERIOD`); a few small reference tables carry no period
# column at all. Grains (keys) differ per dataflow with no shared dimension set,
# so keys are left undeclared.
_TIME = {
    "ksh-0752213b-e937-4722-ae02-b997dabf8453",
    "ksh-093d149c-9951-4dd0-99ae-4a5e858a7b45",
    "ksh-1604a8a4-aea7-4f86-866b-63b1980f77eb",
    "ksh-169201f0-24a4-434a-8900-3c035cd4430f",
    "ksh-33b9d9ea-4fc0-4d9e-a96e-23459adb470b",
    "ksh-5c5c1828-8599-4b96-8b9f-ef6c27ab7c82",
    "ksh-94904cf5-1b76-4c24-9375-65e743668f63",
    "ksh-99ac9e47-dc1b-44d8-8e69-cd88018c0244",
    "ksh-a899cbc1-5223-4310-bd49-e31154f8bdb7",
    "ksh-b4f2e65e-79ee-47e1-8bf0-fa7d14c128ec",
    "ksh-d442dc4c-20fb-4ca8-bfde-9171e04a683d",
    "ksh-d96c6d1d-ee4b-483d-bfab-4b0baaae5e55",
    "ksh-eb3e481e-6b5a-45d1-8076-18c4ece155c2",
}
_TIME_PERIOD = {
    "ksh-168bf117-ad66-4f78-80b5-e3a813b77b37",
    "ksh-1cb63b4f-6dee-4fab-8d54-0d4e1ca884dc",
    "ksh-30c328e3-0b9e-4e34-94f7-6b0fee2fbc53",
    "ksh-3cc11704-5617-446b-ad92-d74c0c081cec",
    "ksh-3d7e51f2-2790-4efc-890a-f2c870b9aa24",
    "ksh-42f7ff87-993f-4a21-b0c2-7c3b179e764f",
    "ksh-43652871-bb56-47ee-8678-6b1dac2fd11b",
    "ksh-6dbf5df3-811e-44ad-8522-a3343dba1ecb",
    "ksh-6dfb5927-57b1-4f71-be7e-4cae406c4862",
    "ksh-7e5f54c0-d50f-496a-ad36-859e0ab7d9e8",
    "ksh-862302dd-8181-438d-ac04-18000851a116",
    "ksh-98128a3b-d7ba-4019-9b18-ac6bcede3104",
    "ksh-a2ec9bac-d0c5-4924-ab84-0a5a0dba3b1b",
    "ksh-ba5fe28d-cbbd-4e66-9d04-895952921544",
    "ksh-bd19297c-4446-4f1e-85de-577a17389793",
    "ksh-c8643d4a-c137-4568-b4ae-990c6dbc948e",
    "ksh-cff5951b-c4d7-434a-8bf7-3786f5a009b1",
    "ksh-e2e2cc46-78b5-4599-82fe-0ed62d6b00d2",
    "ksh-e847b992-6499-4493-9e0a-6899325b8d46",
    "ksh-e962bdbf-4809-4904-808f-9df7d45f0c5e",
    "ksh-f9264f71-aa14-40c6-a561-92f0db28ab0f",
}


def _temporal_for(spec_id):
    if spec_id in _TIME:
        return "TIME"
    if spec_id in _TIME_PERIOD:
        return "TIME_PERIOD"
    return None


# One published Delta table per resource. The dataflows are mutually
# heterogeneous, so the transform is a thin pass that republishes every parsed
# SDMX column; per-dataflow typing is not possible across 38 distinct schemas.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="{}-transform".format(spec.id),
        deps=[spec.id],
        sql='SELECT * FROM "{}"'.format(spec.id),
        **({"temporal": _temporal_for(spec.id)} if _temporal_for(spec.id) else {}),
    )
    for spec in DOWNLOAD_SPECS
]
