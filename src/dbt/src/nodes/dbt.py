"""DBT (UK Department for Business and Trade) Data API connector.

Source: https://data.api.trade.gov.uk (v1), no auth.

Strategy — stateless full re-pull. Each download node fetches one table (or
report) in full from the per-entity data endpoint and saves the raw CSV. The
API exposes a per-table data endpoint that returns the entire table in one
request (no pagination); `latest` 302-redirects to the newest concrete
version, so we always pull the current release and overwrite. There is no
incremental/`since` filter, and re-pulling the whole corpus is cheap (largest
table ~300MB CSV), so no watermark/cursor state is kept.

Format note: the data endpoint serves CSV for every table, but parquet is
NOT generated for some tables (e.g. `measures`, `barriers` 404 with
NoSuchKey). CSV is the one universally-available format, so we fetch CSV
uniformly and let the SQL transform read it via DuckDB read_csv_auto.
Missing values arrive as the literal string "#NA" rather than empty.
"""

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_file, transient_retry

from constants import FETCH_PARAMS

BASE = "https://data.api.trade.gov.uk"


@transient_retry()
def _fetch_csv(url: str) -> bytes:
    # Read timeout is generous: the largest table (tariff measures) is a
    # ~300MB CSV streamed in one response.
    resp = get(url, params={"format": "csv"}, timeout=(10.0, 600.0))
    resp.raise_for_status()
    return resp.content


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    dataset, kind, source_id = FETCH_PARAMS[node_id]
    segment = "tables" if kind == "table" else "reports"
    url = f"{BASE}/v1/datasets/{dataset}/versions/latest/{segment}/{source_id}/data"
    content = _fetch_csv(url)
    # Save the raw CSV bytes straight through — the transform reads it as a
    # DuckDB view. Avoids materializing a multi-million-row arrow table in RAM.
    save_raw_file(content, asset, extension="csv")


DOWNLOAD_SPECS = [
    NodeSpec(id=spec_id, fn=fetch_one, kind="download")
    for spec_id in FETCH_PARAMS
]

# One published Delta table per subset. The source CSV is already the
# publishable shape (one row per entity record); the transform is a
# thin pass-through that also serves as the correctness gate — a 0-row
# result fails the node, catching a silently-empty or reshaped download.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{spec.id}-transform",
        deps=[spec.id],
        sql=f'SELECT * FROM "{spec.id}"',
    )
    for spec in DOWNLOAD_SPECS
]
