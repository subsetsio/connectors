"""North American Breeding Bird Survey (USGS / ScienceBase) connector.

The source publishes a fixed set of distinct-schema tables across two ScienceBase
item families, each released on an annual cadence:

  * the raw observation dataset  — parent item 52b1dfa8e4b0d9b325230cd9, whose
    newest child release holds Routes.csv, Weather.csv, SpeciesList.csv, plus
    States.zip (per-state 10-stop summary counts) and 50-StopData.zip (per-stop
    counts, 1997+).
  * the analysis results        — parent item 5ea835e082cefae35a1fada7, whose
    newest child release holds core/expanded population-trend CSVs and the
    long-format annual abundance-index CSVs.

Fetch strategy (stateless full re-pull — the whole corpus is small and re-pulled
every run; revisions are picked up for free): for each family, query the parent's
children, pick the newest *published* child that carries the expected files, GET
its item JSON to resolve the current content-addressed file download URLs (these
hashes change every release, so they are NEVER hardcoded), then download.

File NAMES drift across releases (case, extension, and embedded year all change —
e.g. routes.csv -> Routes.csv, BBS_1966-2022_core_trend2.csv ->
BBS_Core_Trends_1966-2024.csv), so files are matched by tolerant predicates on the
dynamically-resolved latest item rather than by exact filename.

Raw is written as all-string parquet (CSV cells carry leading-zero codes like AOU
'02010' and StateNum '02', trailing-space padding, and latin-1 text); the
TRANSFORM_SPECS TRIM and TRY_CAST into typed, snake_case published columns. The two
zip-backed tables (state_counts ~0.5GB, fifty_stop_counts ~1.75GB uncompressed) are
streamed chunk-by-chunk through raw_parquet_writer to stay within memory.
"""

import io
import zipfile

import pandas as pd
import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    get,
    transient_retry,
    save_raw_parquet,
    raw_parquet_writer,
)

SLUG = "north-american-breeding-bird-survey"
CATALOG = "https://www.sciencebase.gov/catalog"
RAW_DATASET_PARENT = "52b1dfa8e4b0d9b325230cd9"
ANALYSIS_PARENT = "5ea835e082cefae35a1fada7"
TIMEOUT = (15.0, 300.0)
CHUNK_ROWS = 200_000


# --------------------------------------------------------------------------- #
# HTTP helpers
# --------------------------------------------------------------------------- #
@transient_retry()
def _get_json(url: str) -> dict:
    resp = get(url, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()


@transient_retry()
def _get_bytes(url: str) -> bytes:
    resp = get(url, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.content


# --------------------------------------------------------------------------- #
# ScienceBase resolution
# --------------------------------------------------------------------------- #
def _latest_release(parent_id: str, qualifies) -> str:
    """Id of the newest *published* child item under `parent_id` whose file
    names satisfy `qualifies(names_lower)`. Skips folder/placeholder children
    that carry no matching data files."""
    data = _get_json(
        f"{CATALOG}/items?parentId={parent_id}&format=json&max=50&fields=title,dates,files"
    )
    best = None  # (publication_date_string, item_id)
    for item in data.get("items", []):
        names = [f["name"].lower() for f in (item.get("files") or [])]
        if not qualifies(names):
            continue
        pub = next(
            (d["dateString"] for d in item.get("dates", []) if d.get("type") == "Publication"),
            "",
        )
        cand = (pub, item["id"])
        if best is None or cand > best:
            best = cand
    if best is None:
        raise RuntimeError(f"no qualifying release found under parent {parent_id}")
    return best[1]


def _file_url(item_id: str, matches) -> str:
    """Resolve the current download URL of the first file in `item_id` whose
    name satisfies `matches(name)`."""
    item = _get_json(f"{CATALOG}/item/{item_id}?format=json")
    for f in item.get("files", []):
        if matches(f["name"]):
            return f["url"]
    have = [f["name"] for f in item.get("files", [])]
    raise RuntimeError(f"no file matched in item {item_id}; available: {have}")


def _raw_dataset_item() -> str:
    return _latest_release(
        RAW_DATASET_PARENT,
        lambda names: any(n.startswith("routes") and n.endswith(".csv") for n in names),
    )


def _analysis_item() -> str:
    return _latest_release(
        ANALYSIS_PARENT,
        lambda names: any(_is_index(n) and _is_core(n) for n in names)
        and any(_is_trend(n) and _is_core(n) for n in names),
    )


# Tolerant filename classifiers for the analysis-results CSVs (operate on the
# lowercased name). Naming has varied a lot across releases; these cover the
# historical forms (inde_*, Index_*, *_indices) and the current BBS_* form.
def _is_csv(n: str) -> bool:
    return n.lower().endswith(".csv")


def _is_index(n: str) -> bool:
    n = n.lower()
    return _is_csv(n) and ("indic" in n or "index" in n or "inde_" in n)


def _is_trend(n: str) -> bool:
    n = n.lower()
    return _is_csv(n) and "trend" in n and "decadal" not in n


def _is_core(n: str) -> bool:
    return "core" in n.lower()


def _is_expanded(n: str) -> bool:
    return "expand" in n.lower()


# --------------------------------------------------------------------------- #
# CSV -> parquet writers (all columns kept as strings; typed in the transform)
# --------------------------------------------------------------------------- #
def _download_single_csv(url: str, asset: str) -> None:
    raw = _get_bytes(url)
    df = pd.read_csv(io.BytesIO(raw), dtype=str, keep_default_na=False, encoding="latin-1")
    df.columns = [c.strip() for c in df.columns]
    table = pa.Table.from_pandas(df, preserve_index=False)
    save_raw_parquet(table, asset)


def _stream_zip_csvs(url: str, asset: str, columns: list[str]) -> None:
    """Stream every CSV member of a zip into one parquet asset, chunk by chunk,
    so peak memory is one chunk rather than the (multi-GB) uncompressed total."""
    schema = pa.schema([(c, pa.string()) for c in columns])
    raw = _get_bytes(url)
    with raw_parquet_writer(asset, schema) as writer:
        zf = zipfile.ZipFile(io.BytesIO(raw))
        members = sorted(m for m in zf.namelist() if m.lower().endswith(".csv"))
        if not members:
            raise RuntimeError(f"{asset}: zip at {url} contains no CSV members")
        for member in members:
            with zf.open(member) as fh:
                for chunk in pd.read_csv(
                    fh,
                    dtype=str,
                    keep_default_na=False,
                    encoding="latin-1",
                    chunksize=CHUNK_ROWS,
                ):
                    chunk.columns = [c.strip() for c in chunk.columns]
                    table = pa.Table.from_pandas(
                        chunk[columns], schema=schema, preserve_index=False
                    )
                    writer.write_table(table)


STATE_COLUMNS = [
    "RouteDataID", "CountryNum", "StateNum", "Route", "RPID", "Year", "AOU",
    "Count10", "Count20", "Count30", "Count40", "Count50", "StopTotal", "SpeciesTotal",
]
FIFTY_COLUMNS = [
    "RouteDataID", "CountryNum", "StateNum", "Route", "RPID", "Year", "AOU",
] + [f"Stop{i}" for i in range(1, 51)]


# --------------------------------------------------------------------------- #
# Fetch functions — one access pattern, distinct file targets
# --------------------------------------------------------------------------- #
def fetch_routes(node_id: str) -> None:
    url = _file_url(_raw_dataset_item(), lambda n: n.lower().startswith("routes") and _is_csv(n))
    _download_single_csv(url, node_id)


def fetch_weather(node_id: str) -> None:
    url = _file_url(_raw_dataset_item(), lambda n: n.lower().startswith("weather") and _is_csv(n))
    _download_single_csv(url, node_id)


def fetch_vehicle_data(node_id: str) -> None:
    url = _file_url(
        _raw_dataset_item(),
        lambda n: n.lower().startswith("vehicledata") and _is_csv(n),
    )
    _download_single_csv(url, node_id)


def fetch_species_list(node_id: str) -> None:
    url = _file_url(_raw_dataset_item(), lambda n: n.lower().startswith("specieslist") and _is_csv(n))
    _download_single_csv(url, node_id)


def fetch_state_counts(node_id: str) -> None:
    url = _file_url(
        _raw_dataset_item(),
        lambda n: n.lower().startswith("states") and n.lower().endswith(".zip"),
    )
    _stream_zip_csvs(url, node_id, STATE_COLUMNS)


def fetch_fifty_stop_counts(node_id: str) -> None:
    url = _file_url(
        _raw_dataset_item(),
        lambda n: ("50-stop" in n.lower() or "50stop" in n.lower() or "fifty" in n.lower())
        and n.lower().endswith(".zip"),
    )
    _stream_zip_csvs(url, node_id, FIFTY_COLUMNS)


def fetch_migrant_nonbreeder(node_id: str) -> None:
    url = _file_url(
        _raw_dataset_item(),
        lambda n: "migrantnonbreeder" in n.lower() and n.lower().endswith(".zip"),
    )
    _stream_zip_csvs(url, node_id, FIFTY_COLUMNS)


def fetch_analysis_core_indices(node_id: str) -> None:
    url = _file_url(_analysis_item(), lambda n: _is_index(n) and _is_core(n) and not _is_expanded(n))
    _download_single_csv(url, node_id)


def fetch_analysis_expanded_indices(node_id: str) -> None:
    url = _file_url(_analysis_item(), lambda n: _is_index(n) and _is_expanded(n))
    _download_single_csv(url, node_id)


def fetch_analysis_core_trends(node_id: str) -> None:
    url = _file_url(_analysis_item(), lambda n: _is_trend(n) and _is_core(n) and not _is_expanded(n))
    _download_single_csv(url, node_id)


def fetch_analysis_expanded_trends(node_id: str) -> None:
    url = _file_url(_analysis_item(), lambda n: _is_trend(n) and _is_expanded(n))
    _download_single_csv(url, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-routes", fn=fetch_routes, kind="download"),
    NodeSpec(id=f"{SLUG}-weather", fn=fetch_weather, kind="download"),
    NodeSpec(id=f"{SLUG}-vehicle-data", fn=fetch_vehicle_data, kind="download"),
    NodeSpec(id=f"{SLUG}-species-list", fn=fetch_species_list, kind="download"),
    NodeSpec(id=f"{SLUG}-state-counts", fn=fetch_state_counts, kind="download"),
    NodeSpec(id=f"{SLUG}-fifty-stop-counts", fn=fetch_fifty_stop_counts, kind="download"),
    NodeSpec(id=f"{SLUG}-migrant-nonbreeder", fn=fetch_migrant_nonbreeder, kind="download"),
    NodeSpec(id=f"{SLUG}-analysis-core-indices", fn=fetch_analysis_core_indices, kind="download"),
    NodeSpec(id=f"{SLUG}-analysis-expanded-indices", fn=fetch_analysis_expanded_indices, kind="download"),
    NodeSpec(id=f"{SLUG}-analysis-core-trends", fn=fetch_analysis_core_trends, kind="download"),
    NodeSpec(id=f"{SLUG}-analysis-expanded-trends", fn=fetch_analysis_expanded_trends, kind="download"),
]
