"""IMF connector — SDMX 3.0 Data portal (https://api.imf.org/external/sdmx/3.0).

One published Delta table per IMF dataflow. Each dataflow is fetched in full in a
single request via the SDMX 3.0 data endpoint with the all-series wildcard:

    /data/dataflow/{agencyID}/{dataflowID}/~/*        ('~' = latest, '*' = all keys)

requested as SDMX-CSV 2.0 (flat: dimension columns + TIME_PERIOD + OBS_VALUE +
attribute columns). Payloads are large (CPI alone is ~500MB of CSV), so the fetch
streams the HTTP response line-by-line and writes an all-string Parquet via the
streaming parquet writer — never buffering the whole table in memory. Types are
left as strings in raw (SDMX dimension codes are strings; TIME_PERIOD mixes "2001"
and "2024-M01" forms, which read_csv_auto would mis-type) and cast in the SQL
transform, which is the correctness gate.

Fetch shape: stateless full re-pull every run (shape 1). The portal exposes no
working incremental filter (the documented c[TIME_PERIOD] component filter 400s),
and a full re-pull picks up revisions for free. No state, no watermark.
"""

import csv

import pyarrow as pa
from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    get_client,
    raw_asset_exists,
    raw_parquet_writer,
    transient_retry,
)


BASE = "https://api.imf.org/external/sdmx/3.0"
CSV_ACCEPT = "application/vnd.sdmx.data+csv;version=2.0.0"
HEADERS = {"Accept": CSV_ACCEPT}

# SDMX-CSV structural columns carry no per-observation information (STRUCTURE is
# always 'dataflow', STRUCTURE_ID the flow urn, ACTION always 'R'). DuckDB names
# the first column literally 'STRUCTURE[;]'. Drop all of them from raw.
DROP_COLS = {"STRUCTURE[;]", "STRUCTURE", "STRUCTURE_ID", "ACTION"}

# Rows per Parquet batch — bounds memory while keeping files few. ~100k string
# rows of ~20 columns is well under the spawn-subprocess RSS ceiling.
BATCH_ROWS = 100_000

# Entity union (rank-active dataflows) -> SDMX agency id. The agency is part of
# the data URL path, so it must travel with the id. Copied from the entity union
# joined with the collect catalog's agencyID.
ENTITIES = {
    "AEA": "IMF.STA",
    "AFRREO": "IMF.AFR",
    "ANEA": "IMF.STA",
    "APDREO": "IMF.APD",
    "BOP": "IMF.STA",
    "BOP_AGG": "IMF.STA",
    "CCI": "IMF.STA",
    "CO2E": "IMF.STA",
    "COFER": "IMF.STA",
    "CPI": "IMF.STA",
    "CPI_WCA": "IMF.STA",
    "CTOT": "IMF.RES",
    "DIP": "IMF.STA",
    "ED": "IMF.RES",
    "EER": "IMF.STA",
    "ENVTX": "IMF.STA",
    "EQ": "IMF.RES",
    "ER": "IMF.STA",
    "ESG_FINANCE": "IMF.STA",
    "ESG_FINANCE_CURRENCY": "IMF.STA",
    "ESG_FINANCE_ISSUER": "IMF.STA",
    "FA": "IMF.STA",
    "FAS": "IMF.STA",
    "FD": "IMF.STA",
    "FDI": "IMF.MCM",
    "FFS": "IMF.STA",
    "FM": "IMF.FAD",
    "FSIBSIS": "IMF.STA",
    "FSIC": "IMF.STA",
    "FSICDM": "IMF.STA",
    "GDD": "IMF.FAD",
    "GENENVPROEXP": "IMF.STA",
    "GFS_BS": "IMF.STA",
    "GFS_COFOG": "IMF.STA",
    "GFS_SFCP": "IMF.STA",
    "GFS_SOEF": "IMF.STA",
    "GFS_SOO": "IMF.STA",
    "GFS_SSUC": "IMF.STA",
    "GS_ATF": "IMF.STA",
    "GS_CGI": "IMF.STA",
    "GS_ED": "IMF.STA",
    "GS_HEALTH": "IMF.STA",
    "GS_LEPM": "IMF.STA",
    "GS_LGRGHTS": "IMF.STA",
    "GS_LI": "IMF.STA",
    "GS_SDO": "IMF.STA",
    "HPD": "IMF.FAD",
    "ICSD": "IMF.FAD",
    "IIP": "IMF.STA",
    "IIPCC": "IMF.STA",
    "IL": "IMF.STA",
    "IMTS": "IMF.STA",
    "IRFCL": "IMF.STA",
    "ISORA_LATEST_DATA_PUB": "ISORA",
    "ITG": "IMF.STA",
    "ITG_WCA_2026_FEB_VINTAGE": "IMF.STA",
    "ITS": "IMF.RES",
    "LS": "IMF.STA",
    "MCDREO": "IMF.MCD",
    "MFS_CBS": "IMF.STA",
    "MFS_DC": "IMF.STA",
    "MFS_FC": "IMF.STA",
    "MFS_FMP": "IMF.STA",
    "MFS_IR": "IMF.STA",
    "MFS_MA": "IMF.STA",
    "MFS_NSRF": "IMF.STA",
    "MFS_ODC": "IMF.STA",
    "MFS_OFC": "IMF.STA",
    "NDGAIN": "IMF.STA",
    "NSDP": "IMF.STA",
    "PCPS": "IMF.RES",
    "PI": "IMF.STA",
    "PIP": "IMF.STA",
    "PI_WCA": "IMF.STA",
    "PPI": "IMF.STA",
    "PSBS": "IMF.FAD",
    "QGDP_WCA": "IMF.STA",
    "QGFS": "IMF.STA",
    "QNEA": "IMF.STA",
    "RE": "IMF.STA",
    "RSUI": "IMF.WHD",
    "SPE": "IMF.STA",
    "SRD": "IMF.RES",
    "TEG": "IMF.STA",
    "UNFCCC": "IMF.STA",
    "WEO": "IMF.RES",
    "WHDREO": "IMF.WHD",
    "WORLD": "IMF.FAD",
}


def _node_id(entity_id: str) -> str:
    return f"imf-{entity_id.lower().replace('_', '-')}"


# Reverse map node_id -> (entity_id, agency) so the single-arg fetch fn can
# recover the original dataflow id (the lower/replace transform is lossy).
NODE_TO_ENTITY = {_node_id(eid): (eid, agency) for eid, agency in ENTITIES.items()}


def _rows_to_table(rows, keep_idx, keep_names, schema):
    """Transpose a batch of CSV rows into an all-string pa.Table. Empty fields
    become NULL; short rows pad with NULL."""
    columns = [[] for _ in keep_idx]
    for row in rows:
        ln = len(row)
        for j, i in enumerate(keep_idx):
            v = row[i] if i < ln else None
            columns[j].append(v if v else None)
    arrays = [pa.array(col, type=pa.string()) for col in columns]
    return pa.Table.from_arrays(arrays, schema=schema)


@transient_retry()
def _download_dataflow(asset: str, url: str) -> int:
    """Stream the dataflow's SDMX-CSV and write it to an all-string Parquet.

    Returns the number of data rows written. Re-runs cleanly on retry: the
    parquet writer reopens (truncates) the asset each attempt.
    """
    client = get_client()
    with client.stream("GET", url, headers=HEADERS, timeout=(10.0, 300.0)) as resp:
        resp.raise_for_status()
        lines = resp.iter_lines()
        try:
            header = next(lines)
        except StopIteration:
            raise RuntimeError(f"{asset}: empty response (no header row)")
        cols = next(csv.reader([header]))
        keep_idx = [i for i, c in enumerate(cols) if c not in DROP_COLS]
        keep_names = [cols[i] for i in keep_idx]
        schema = pa.schema([(n, pa.string()) for n in keep_names])

        n_rows = 0
        with raw_parquet_writer(asset, schema) as w:
            batch = []
            for row in csv.reader(lines):
                if not row:
                    continue
                batch.append(row)
                if len(batch) >= BATCH_ROWS:
                    w.write_table(_rows_to_table(batch, keep_idx, keep_names, schema))
                    n_rows += len(batch)
                    batch = []
            if batch:
                w.write_table(_rows_to_table(batch, keep_idx, keep_names, schema))
                n_rows += len(batch)
    return n_rows


def fetch_one(node_id: str) -> None:
    asset = node_id  # the spec id IS the asset name
    entity_id, agency = NODE_TO_ENTITY[node_id]
    url = f"{BASE}/data/dataflow/{agency}/{entity_id}/~/*"
    n = _download_dataflow(asset, url)
    print(f"[imf] {asset}: wrote {n} rows from {url}")


DOWNLOAD_SPECS = [
    NodeSpec(id=_node_id(eid), fn=fetch_one, kind="download")
    for eid in ENTITIES
]


# Freshness policy: the full per-dataflow re-pull is expensive (the whole corpus
# is ~1-2 hours of streaming CSV), while the fastest IMF release cadence for
# these dataflows is monthly. The SDMX 3.0 portal exposes no reliable
# incremental filter (the documented c[TIME_PERIOD] component 400s) and no
# per-dataflow validator header we can trust, so skip on raw age: refetch a
# dataflow only when its committed raw is older than ~25 days (about one monthly
# release). FORCE_REFRESH=1 bypasses this. (inferred cadence — no single
# published schedule spans all dataflows.)
MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=_node_id(eid),
        description=(
            "IMF SDMX 3.0 dataflow; monthly-or-slower releases. Skip refetch "
            "while committed raw is younger than 25 days (inferred — no single "
            "published cadence)."
        ),
        check=lambda aid: raw_asset_exists(aid, "parquet", max_age_days=25),
    )
    for eid in ENTITIES
]
