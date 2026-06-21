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

# One published Delta table per resource. The dataflows are mutually
# heterogeneous, so the transform is a thin pass that republishes every parsed
# SDMX column; per-dataflow typing is not possible across 38 distinct schemas.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="{}-transform".format(spec.id),
        deps=[spec.id],
        sql='SELECT * FROM "{}"'.format(spec.id),
    )
    for spec in DOWNLOAD_SPECS
]
