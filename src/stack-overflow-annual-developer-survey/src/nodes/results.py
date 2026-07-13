"""Stack Overflow Annual Developer Survey -- per-year results micro-data.

Mechanism: github_archive_csv (bulk per-entity download). Each release year
(2011-2025) ships a `results.csv` (anonymized individual respondent micro-data).

Shape: stateless full re-pull (decision shape 1). Each year's file is a small,
immutable yearly snapshot (largest ~196MB); re-fetching the whole corpus every
run is cheap and picks up any newly-published year for free. No watermark, no
cursor -- there is no incremental delta filter and none is needed.

Modeling: the survey's question set is revised every year, so each year's
results table has a DISTINCT column list. Hence one published table per year
(15 `results-<year>` subsets) rather than a merged table. Because early years
(2011-2014) use full question text as column headers, headers are sanitized to
Delta-safe identifiers in the fetch fn. Every results column is kept as a
string: the per-year schemas are wide (65-114 cols) and mix free-text,
multi-select, and numeric answers, so a uniform string projection always loads
and never fights per-year type drift; downstream consumers cast as needed.
"""
import re

from subsets_utils import NodeSpec, save_raw_parquet

from utils import RAW_BASE, fetch_bytes, read_csv

SLUG = "stack-overflow-annual-developer-survey"

# Entity union (rank-active), copied verbatim from work/entity_union.json.
from constants import RESULTS_YEARS


def _safe_columns(columns) -> list[str]:
    """Map arbitrary CSV headers to unique Delta-safe identifiers.

    Clean code-style headers (ResponseId, MainBranch) pass through unchanged;
    early-year question-text headers ('What Country...?') collapse to
    underscore-joined identifiers. Delta (no column mapping) rejects spaces and
    punctuation in column names, so only [A-Za-z0-9_] survive.
    """
    used: set[str] = set()
    out: list[str] = []
    for raw in columns:
        s = re.sub(r"[^0-9A-Za-z]+", "_", str(raw)).strip("_")
        if not s:
            s = "col"
        if s[0].isdigit():
            s = "c_" + s
        base, i = s, 2
        while s in used:
            s = f"{base}_{i}"
            i += 1
        used.add(s)
        out.append(s)
    return out


def fetch_results(node_id: str) -> None:
    """Fetch one year's results.csv and write it as an all-string parquet."""
    # Heavy deps imported inside the fn: keeps the module top-level free of
    # numpy/pandas so spec introspection (which runs with the harness dir on
    # sys.path, shadowing stdlib `secrets`) imports cleanly.
    import pyarrow as pa

    asset = node_id  # the runtime passes the spec id; it IS the asset name
    year = node_id.rsplit("-", 1)[-1]
    content = fetch_bytes(f"{RAW_BASE}/{year}/results.csv")

    # dtype=str → uniform string columns; blank cells stay NaN -> null in
    # parquet. Encoding fallback handles the early cp1252-era files.
    df = read_csv(content, low_memory=False)

    # Early-year surveys (2011-2014) use a wide multi-select matrix layout that
    # leaves many blank-header option-slot columns entirely empty; pandas names
    # them "Unnamed: N". Drop only those that carry no information (<=1 distinct
    # non-null value) — this keeps blank-header columns that DO hold real data
    # (multi-select answers, the 2016 respondent-index column) untouched.
    drop = [
        c for c in df.columns
        if str(c).startswith("Unnamed:") and df[c].nunique(dropna=True) <= 1
    ]
    if drop:
        df = df.drop(columns=drop)

    df.columns = _safe_columns(df.columns)

    schema = pa.schema([(c, pa.string()) for c in df.columns])
    table = pa.Table.from_pandas(df, schema=schema, preserve_index=False)
    save_raw_parquet(table, asset)


_RESULTS_DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-results-{year}", fn=fetch_results, kind="download")
    for year in RESULTS_YEARS
]
