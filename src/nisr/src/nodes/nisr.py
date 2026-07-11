"""NISR (National Institute of Statistics of Rwanda) connector.

Open machine-readable surface = the NADA Central Data Catalog
(microdata.statistics.gov.rw). Two published tables, both metadata/reference
(the underlying survey microdata is access-gated and the indicator portal is
Cloudflare-blocked — see research):

  * nisr-studies   — one row per NISR study (survey/census), from the catalog
                     CSV export (single request, whole catalog).
  * nisr-variables — long-format variable codebook, one row per (study, variable),
                     parsed from each study's DDI-Codebook XML (catalog/ddi/{id}).

Fetch shape: stateless full re-pull. The corpus is tiny (~75 studies, no
server-side incremental filter), so we re-fetch everything every run and
overwrite.
"""
import io
import csv
import xml.etree.ElementTree as ET

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    get,
    transient_retry,
    save_raw_parquet,
    save_raw_ndjson,
)

CATALOG_CSV_URL = "https://microdata.statistics.gov.rw/index.php/catalog/export/csv?ps=5000"
DDI_URL = "https://microdata.statistics.gov.rw/index.php/catalog/ddi/{id}"

# Catalog CSV columns (verified). Kept as strings in raw; cast in transform.
STUDY_COLUMNS = [
    "id",
    "surveyid",
    "titl",
    "nation",
    "authenty",
    "data_coll_start",
    "data_coll_end",
    "created",
    "changed",
]
STUDIES_SCHEMA = pa.schema([(c, pa.string()) for c in STUDY_COLUMNS])

# sumStat @type -> output column for the variable codebook.
SUMSTAT_FIELDS = {
    "vald": "stat_valid",
    "invd": "stat_invalid",
    "min": "stat_min",
    "max": "stat_max",
    "mean": "stat_mean",
    "stdev": "stat_stdev",
}


def _localname(el) -> str:
    return el.tag.rsplit("}", 1)[-1]


@transient_retry()
def _fetch_bytes(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.content


def _load_catalog_rows() -> list[dict]:
    raw = _fetch_bytes(CATALOG_CSV_URL).decode("utf-8-sig")
    rows = list(csv.DictReader(io.StringIO(raw)))
    # Normalize to exactly the declared columns (missing -> empty string).
    out = []
    for r in rows:
        out.append({c: (r.get(c) or "").strip() for c in STUDY_COLUMNS})
    return out


def fetch_studies(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    rows = _load_catalog_rows()
    if not rows:
        raise AssertionError("NISR catalog CSV returned no study rows")
    table = pa.Table.from_pylist(rows, schema=STUDIES_SCHEMA)
    save_raw_parquet(table, asset)


def _parse_ddi_variables(xml_bytes: bytes, study: dict) -> list[dict]:
    root = ET.fromstring(xml_bytes)
    out = []
    for v in (e for e in root.iter() if _localname(e) == "var"):
        row = {
            "study_id": study["id"],
            "surveyid": study["surveyid"],
            "study_title": study["titl"],
            "var_id": v.get("ID"),
            "name": v.get("name"),
            "intrvl": v.get("intrvl"),
            "decimals": v.get("dcml"),
            "label": None,
            "format_type": None,
        }
        for col in SUMSTAT_FIELDS.values():
            row[col] = None
        for child in v:
            ln = _localname(child)
            if ln == "labl" and child.text:
                row["label"] = child.text.strip()
            elif ln == "varFormat":
                row["format_type"] = child.get("type")
            elif ln == "sumStat":
                col = SUMSTAT_FIELDS.get(child.get("type"))
                if col and child.text:
                    row[col] = child.text.strip()
        out.append(row)
    return out


def fetch_variables(node_id: str) -> None:
    asset = node_id
    studies = _load_catalog_rows()
    rows: list[dict] = []
    for study in studies:
        sid = study["id"]
        if not sid.isdigit():
            continue
        try:
            xml_bytes = _fetch_bytes(DDI_URL.format(id=sid))
        except Exception as exc:  # permanent fetch failure for one study -> skip it
            print(f"nisr-variables: skipping study {sid}: {type(exc).__name__}: {exc}")
            continue
        try:
            rows.extend(_parse_ddi_variables(xml_bytes, study))
        except ET.ParseError as exc:
            print(f"nisr-variables: unparseable DDI for study {sid}: {exc}")
            continue
    if not rows:
        raise AssertionError("parsed zero variables across all NISR studies")
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="nisr-studies", fn=fetch_studies, kind="download"),
    NodeSpec(id="nisr-variables", fn=fetch_variables, kind="download"),
]
