"""Electoral Integrity Project (EIP) — Perceptions of Electoral Integrity (PEI).

Source: the dedicated "PEI" Harvard Dataverse collection
(https://dataverse.harvard.edu/dataverse/PEI), accessed via the Dataverse
native REST API (no auth). The flagship product is the cumulative global
release (PEI-N.0), which ships two tabular files:

  - Election-level aggregate ("PEI_N Election External"): one row per national
    contest, carrying the 100-point PEI integrity index and its sub-dimensions.
  - Expert-level micro file ("PEI_N Expert External"): one row per expert
    survey response.

Fetch shape: stateless full re-pull (shape 1). The whole corpus is two files,
a few MB each, re-fetchable in seconds; releases are immutable and new data
arrives as a NEW dataset version, so we re-resolve the latest global release
each run (picking up PEI-12.0 etc. for free) rather than tracking a watermark.
There is no incremental query on the Data Access API. Each tabular file is
Dataverse-ingested to a .tab (TSV) with a stable header row; we download the
.tab, parse with pandas (column-type inference over a single full snapshot),
and save a typed parquet. dataFile ids change between release versions, so they
are resolved fresh from the collection metadata on every run.
"""
import re
from io import BytesIO


from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

BASE = "https://dataverse.harvard.edu/api"
COLLECTION = "PEI"


@transient_retry()
def _get_json(url: str, **params) -> dict:
    resp = get(url, params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


@transient_retry()
def _get_bytes(url: str, **params) -> bytes:
    resp = get(url, params=params, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def _title(version: dict) -> str:
    for f in version.get("metadataBlocks", {}).get("citation", {}).get("fields", []):
        if f.get("typeName") == "title":
            return f.get("value", "")
    return ""


def _is_country_substudy(title: str) -> bool:
    t = title.lower()
    return bool(
        re.search(r"\bus\b|_us_|- us", t)
        or "uk" in t
        or "mexico" in t
        or "russia" in t
    )


def _version(title: str) -> float:
    m = re.search(r"(\d+\.\d+)", title)
    return float(m.group(1)) if m else 0.0


def _latest_global_version() -> dict:
    """Resolve the latestVersion metadata of the highest-numbered global
    cumulative PEI release in the collection. Raises if none found (a real
    failure worth surfacing, not a silent skip)."""
    contents = _get_json(f"{BASE}/dataverses/{COLLECTION}/contents")["data"]
    dois = [
        f"{d['protocol']}:{d['authority']}/{d['identifier']}"
        for d in contents
        if d.get("type") == "dataset"
    ]
    best = None
    for doi in dois:
        ver = _get_json(
            f"{BASE}/datasets/:persistentId/", persistentId=doi
        )["data"]["latestVersion"]
        title = _title(ver)
        if _is_country_substudy(title):
            continue
        v = _version(title)
        if best is None or v > best[0]:
            best = (v, title, ver)
    if best is None:
        raise RuntimeError(
            "no global PEI release found in the PEI Dataverse collection"
        )
    return best[2]


def _pick_tab_file_id(version: dict, keyword: str) -> int:
    """Find the dataFile id of the .tab (Dataverse-ingested TSV) file whose
    label identifies the requested table type ('election' or 'expert')."""
    for f in version.get("files", []):
        label = f["label"].lower()
        if keyword in label and label.endswith(".tab"):
            return f["dataFile"]["id"]
    raise RuntimeError(
        f"no .tab file matching '{keyword}' in latest global PEI release"
    )


def fetch_one(node_id: str) -> None:
    # Imported inside the fn (not at module level) to keep the harness's
    # spec-introspection import light and avoid a numpy `import secrets`
    # shadowing collision in the introspection path; the cloud run is clean.
    import pandas as pd
    import pyarrow as pa

    asset = node_id  # the spec id IS the asset name
    entity = node_id[len("electoral-integrity-project-"):]  # pei-election / pei-expert
    keyword = "election" if "election" in entity else "expert"

    version = _latest_global_version()
    file_id = _pick_tab_file_id(version, keyword)

    content = _get_bytes(f"{BASE}/access/datafile/{file_id}")
    df = pd.read_csv(BytesIO(content), sep="\t", low_memory=False)
    if df.empty:
        raise RuntimeError(f"{asset}: downloaded .tab parsed to 0 rows")

    table = pa.Table.from_pandas(df, preserve_index=False)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="electoral-integrity-project-pei-election", fn=fetch_one, kind="download"),
    NodeSpec(id="electoral-integrity-project-pei-expert", fn=fetch_one, kind="download"),
]

# Thin parse-and-type pass: the raw parquet is already typed by pandas; publish
# the full official table, normalizing the two obvious columns (year is stored
# as a float like 2014.0; date as an ISO string) via TRY_CAST so a stray value
# becomes NULL rather than failing the node. Rows must carry a contest id.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT * REPLACE (
                TRY_CAST(year AS INTEGER) AS year,
                TRY_CAST(date AS DATE) AS date
            )
            FROM "{s.id}"
            WHERE election IS NOT NULL
        ''',
    )
    for s in DOWNLOAD_SPECS
]
