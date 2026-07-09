"""Penn World Table (PWT) connector.

Source: Groningen Growth and Development Centre (GGDC), University of Groningen,
published as a single DataverseNL dataset (DOI 10.34894/FABVLR, currently
PWT 11.0 — 185 countries, 1950-2023).

Mechanism: Dataverse native REST API. The dataset's file manifest is read from
/api/datasets/:persistentId/ and each table is fetched in full via
/api/access/datafile/{id} (303-redirects to a signed S3 URL). Files are served
as original Stata (.dta) binaries; we parse them with pandas.read_stata and
persist parquet so the SQL transforms can read them.

Strategy: stateless full re-pull. The whole corpus is ~40MB and a static
versioned release, so every run re-fetches all six tables in full and
overwrites. The datafile ids change when GGDC publishes a new PWT version, so
ids are always re-resolved from the manifest rather than hardcoded.

Six publishable tables, one download + one transform each:
  main                  country-year panel, ~50 income/output/productivity vars
  na_data               national-accounts series per country-year
  capital_detail        capital stocks/investment/depreciation by asset type
  labor_detail          human-capital and labor-share detail
  trade_detail          export/import price-levels and cost shares
  sh_bilateral_cor_data bilateral (country-pair) export-correlation data
"""

import re


from subsets_utils import (
    NodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

DOI = "doi:10.34894/FABVLR"
DATASET_API = "https://dataverse.nl/api/datasets/:persistentId/?persistentId=" + DOI
ACCESS_API = "https://dataverse.nl/api/access/datafile/{id}"

# Entity union — the six rank-active subsets. Keys are the collect entity ids;
# the spec id for each is f"penn-world-table-{id.replace('_','-')}".
ENTITY_IDS = [
    "main",
    "na_data",
    "capital_detail",
    "labor_detail",
    "trade_detail",
    "sh_bilateral_cor_data",
]


def _file_role(label: str) -> str:
    """Logical, version-stable role for a Dataverse file label.

    Strips the leading 'pwt<NN>' prefix and the extension so that e.g.
    'pwt110_na_data.dta' -> 'na_data' and 'pwt110.dta' -> 'main'. Mirrors the
    collect stage's slugging so ids stay aligned across PWT versions.
    """
    stem = label.rsplit(".", 1)[0]
    role = re.sub(r"^pwt\d+_?", "", stem)
    return role or "main"


@transient_retry()
def _get_json(url: str) -> dict:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


@transient_retry()
def _get_bytes(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def _resolve_dta_file_ids() -> dict[str, int]:
    """Map logical role -> Dataverse datafile id for every .dta data file in the
    current release, read live from the manifest."""
    manifest = _get_json(DATASET_API)
    files = manifest["data"]["latestVersion"]["files"]
    role_to_id: dict[str, int] = {}
    for f in files:
        label = f.get("label") or f["dataFile"].get("filename", "")
        if not label.lower().endswith(".dta"):
            continue
        role_to_id[_file_role(label)] = f["dataFile"]["id"]
    return role_to_id


def fetch_one(node_id: str) -> None:
    import io

    import pandas as pd
    import pyarrow as pa

    asset = node_id  # the spec id IS the asset name
    role = node_id[len("penn-world-table-"):].replace("-", "_")

    role_to_id = _resolve_dta_file_ids()
    if role not in role_to_id:
        raise KeyError(
            f"PWT release manifest has no .dta for role '{role}'; "
            f"available roles: {sorted(role_to_id)}"
        )

    raw = _get_bytes(ACCESS_API.format(id=role_to_id[role]))
    df = pd.read_stata(io.BytesIO(raw))
    # Stata column labels can carry value-label categoricals; flatten to plain
    # strings/values so parquet typing is unambiguous.
    df = df.convert_dtypes(dtype_backend="numpy_nullable")
    table = pa.Table.from_pandas(df, preserve_index=False)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"penn-world-table-{eid.replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]
