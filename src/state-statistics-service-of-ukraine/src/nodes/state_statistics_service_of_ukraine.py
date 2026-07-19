"""State Statistics Service of Ukraine SDMX downloads.

Each accepted entity is one SSSU SDMX dataflow. Dataflows have different DSDs,
so the raw download preserves the source SDMX-CSV response exactly and lets the
model stage profile each table's observed columns.
"""

from datetime import datetime
import csv
import gzip
import io
import os
import re

import pyarrow as pa
import pyarrow.csv as pacsv

from constants import ENTITY_IDS
from subsets_utils import (
    NodeSpec,
    delete_raw_file,
    get,
    list_raw_fragments,
    save_raw_file,
    save_raw_parquet,
)

SLUG = "state-statistics-service-of-ukraine"
SDMX_BASE = "https://stat.gov.ua/sdmx/workspaces/default:integration/registry/sdmx/2.1"
SDMX3_BASE = "https://stat.gov.ua/sdmx/workspaces/default:integration/registry/sdmx/3.0"

CSV_HEADERS = {
    "Accept": "text/csv",
    "Accept-Language": "en",
}

# Bounds on the key-slicing fallback: never split a dimension so wide that the
# splitting costs more requests than the slice, and stop descending eventually.
MAX_SPLIT_VALUES = 500
MAX_SPLIT_DEPTH = 4

_SPEC_TO_ENTITY = {
    f"{SLUG}-{entity_id.lower().replace('_', '-')}": entity_id
    for entity_id in ENTITY_IDS
}

_LATEST_VERSIONS: dict[str, str] = {}

_RETIRED_HINT = {
    # Folded into DF_EXTERNAL_TRADE_OF_GOODS_M_Q, which carries both frequencies.
    "DF_EXTERNAL_TRADE_OF_GOODS_M": "DF_EXTERNAL_TRADE_OF_GOODS_M_Q",
}

_CSV_GZIP_RAW = {
    # This flow is too large to finish reliably when every slice is converted
    # through Arrow into Parquet during the download node. The transform runtime
    # reads csv.gz fragments directly, and this keeps the source payload shape.
    "DF_EXTERNAL_TRADE_OF_GOODS_M_Q",
}


def _latest_version(entity_id: str) -> str:
    """The dataflow's current version, resolved from the registry per run.

    SSSU publishes every revision as a NEW dataflow version and freezes the old
    one rather than updating it in place, so a pinned version silently decays
    into a snapshot: v6 of DF_PROD_SOLD_INDUSTRIAL_PRODUCTS_TYPE still answers,
    but stops a year short of the live v12. Retired flows disappear outright.
    Bare `dataflow/SSSU` returns exactly one entry per id — the latest.
    """
    if not _LATEST_VERSIONS:
        response = get(
            f"{SDMX_BASE}/dataflow/SSSU",
            headers={"Accept": "application/json"},
            timeout=(10.0, 120.0),
        )
        response.raise_for_status()
        dataflows = response.json().get("data", {}).get("dataflows", [])
        if not dataflows:
            raise ValueError("SSSU dataflow registry returned no dataflows")
        _LATEST_VERSIONS.update({item["id"]: item["version"] for item in dataflows})

    if entity_id not in _LATEST_VERSIONS:
        hint = _RETIRED_HINT.get(entity_id)
        succeeded_by = f"; superseded by {hint}" if hint else ""
        raise ValueError(
            f"{entity_id}: retired upstream - absent from the SSSU dataflow registry{succeeded_by}"
        )
    return _LATEST_VERSIONS[entity_id]


def _looks_like_sdmx_csv(content: bytes) -> bool:
    head = content[:4096].decode("utf-8-sig", "replace")
    return "DATAFLOW" in head and "TIME_PERIOD" in head and "OBS_VALUE" in head and "\n" in head


def _normalized_sdmx_csv(content: bytes) -> tuple[bytes, int]:
    text = content.decode("utf-8-sig", "replace")
    reader = csv.reader(io.StringIO(text))
    rows = []
    columns = None
    for row in reader:
        row = [" ".join(cell.split()) for cell in row]
        if not row or not any(cell.strip() for cell in row):
            continue
        if columns is None:
            columns = row
            rows.append(row)
            continue
        if len(row) == len(columns):
            rows.append(row)

    if columns is None:
        return b"", 0

    output = io.StringIO()
    writer = csv.writer(output, lineterminator="\n")
    writer.writerows(rows)
    return output.getvalue().encode("utf-8"), max(len(rows) - 1, 0)


def _csv_row_count(content: bytes) -> int:
    _, row_count = _normalized_sdmx_csv(content)
    return row_count


def _csv_to_table(normalized: bytes) -> pa.Table:
    if not normalized:
        raise ValueError("SDMX-CSV response had no header")
    header = normalized.splitlines()[0].decode("utf-8")
    columns = next(csv.reader(io.StringIO(header)))
    return pacsv.read_csv(
        pa.BufferReader(normalized),
        read_options=pacsv.ReadOptions(encoding="utf8"),
        convert_options=pacsv.ConvertOptions(
            column_types={column: pa.string() for column in columns},
            strings_can_be_null=True,
        ),
    )


def _save_sdmx_csv(
    content: bytes,
    node_id: str,
    *,
    fragment: str | None = None,
    csv_gzip: bool = False,
) -> int:
    normalized, row_count = _normalized_sdmx_csv(content)
    if row_count == 0:
        return 0
    if csv_gzip:
        save_raw_file(
            gzip.compress(normalized, compresslevel=1),
            node_id,
            "csv.gz",
            fragment=fragment,
        )
        return row_count
    save_raw_parquet(_csv_to_table(normalized), node_id, fragment=fragment)
    return row_count


def _save_retired_marker(entity_id: str, node_id: str) -> None:
    """Commit an empty raw asset for a waived dataflow retired by SSSU."""
    table = pa.table(
        {
            "DATAFLOW": pa.array([], type=pa.string()),
            "TIME_PERIOD": pa.array([], type=pa.string()),
            "OBS_VALUE": pa.array([], type=pa.string()),
            "RETIRED_UPSTREAM": pa.array([], type=pa.string()),
        }
    )
    save_raw_parquet(table, node_id)
    print(f"  -> {entity_id} is retired upstream; saved empty waived marker")


def _year(value: str) -> int:
    match = re.search(r"\d{4}", value or "")
    if not match:
        raise ValueError(f"cannot read year from availability value {value!r}")
    return int(match.group(0))


def _availability(entity_id: str, version: str, key: str | None = None) -> dict:
    path = f"{entity_id}/{version}" if key is None else f"{entity_id}/{version}/{key}"
    url = f"{SDMX3_BASE}/availability/dataflow/SSSU/{path}/all"
    response = get(url, headers={"Accept": "application/json"}, timeout=(10.0, 120.0))
    response.raise_for_status()
    payload = response.json()
    constraints = payload.get("data", {}).get("dataConstraints", [])
    if not constraints:
        raise ValueError(f"{entity_id}: availability response has no data constraints")
    return constraints[0]


def _availability_years(entity_id: str, version: str) -> range:
    annotations = _availability(entity_id, version).get("annotations", [])
    metrics = {
        item.get("id"): item.get("title")
        for item in annotations
        if item.get("type") == "sdmx_metrics"
    }
    start = _year(metrics.get("time_period_start", ""))
    end = min(_year(metrics.get("time_period_end", "")), datetime.utcnow().year)
    if end < start:
        raise ValueError(f"{entity_id}: invalid availability range {start}..{end}")
    return range(start, end + 1)


def _availability_values(
    entity_id: str, version: str, key: str | None = None
) -> dict[str, list[str]]:
    """Per-slice allowed values, keyed by dimension id."""
    regions = _availability(entity_id, version, key).get("cubeRegions", [])
    if not regions:
        return {}
    return {
        component["id"]: [value["value"] for value in component.get("values", [])]
        for component in regions[0].get("components", [])
    }


def _dimension_order(entity_id: str, version: str) -> list[str]:
    """Key dimension ids in DSD position order (the dotted key's slot order)."""
    url = f"{SDMX_BASE}/dataflow/SSSU/{entity_id}/{version}"
    response = get(url, headers={"Accept": "application/json"}, timeout=(10.0, 120.0))
    response.raise_for_status()
    dataflows = response.json().get("data", {}).get("dataflows", [])
    if not dataflows:
        raise ValueError(f"{entity_id}: dataflow {version} not found upstream")

    match = re.search(r"DataStructure=([^:]+):([^(]+)\(([^)]+)\)", dataflows[0]["structure"])
    if not match:
        raise ValueError(f"{entity_id}: cannot read DSD from {dataflows[0]['structure']!r}")
    agency, dsd_id, dsd_version = match.groups()

    dsd_url = f"{SDMX_BASE}/datastructure/{agency}/{dsd_id}/{dsd_version}?references=none"
    dsd_response = get(dsd_url, headers={"Accept": "application/json"}, timeout=(10.0, 120.0))
    dsd_response.raise_for_status()
    structures = dsd_response.json().get("data", {}).get("dataStructures", [])
    if not structures:
        raise ValueError(f"{entity_id}: DSD {dsd_id} {dsd_version} not found upstream")
    dimensions = structures[0]["dataStructureComponents"]["dimensionList"]["dimensions"]
    return [item["id"] for item in sorted(dimensions, key=lambda item: item["position"])]


def _fetch_csv(url: str) -> bytes | None:
    response = get(url, headers=CSV_HEADERS, timeout=(10.0, 900.0))
    if response.status_code >= 400:
        return None
    content = response.content
    if not _looks_like_sdmx_csv(content):
        return None
    return content


def _fragment_name(dimensions: list[str], key_parts: list[str]) -> str:
    return "__".join(
        f"{dimension.lower()}-{re.sub(r'[^0-9A-Za-z_]+', '-', value)}"
        for dimension, value in zip(dimensions, key_parts)
        if value
    )


def _fetch_key_slices(
    entity_id: str,
    version: str,
    node_id: str,
    dimensions: list[str],
    key_parts: list[str],
    depth: int,
    csv_gzip: bool = False,
    done_fragments: set[str] | None = None,
) -> int:
    """Fetch one key slice, splitting on a dimension when the server can't build it.

    SSSU answers 500 for slices that are too large to render, and the size is
    driven by the series count rather than the time range — so a slice that the
    yearly requests can't shrink is split along its own availability instead.

    An all-empty key goes straight to the split: that request is the unsliced one
    `fetch_one` has already tried.
    """
    # Both endpoints want the key omitted entirely rather than left all-empty.
    key = ".".join(key_parts) if any(key_parts) else None
    if key is not None:
        fragment = _fragment_name(dimensions, key_parts)
        if done_fragments is not None and fragment in done_fragments:
            return 1
        content = _fetch_csv(f"{SDMX_BASE}/data/SSSU,{entity_id},{version}/{key}")
        if content is not None:
            row_count = _save_sdmx_csv(
                content,
                node_id,
                fragment=fragment,
                csv_gzip=csv_gzip,
            )
            if row_count:
                if done_fragments is not None:
                    done_fragments.add(fragment)
                return 1
            return 0

    if depth >= MAX_SPLIT_DEPTH:
        return 0

    available = _availability_values(entity_id, version, key)
    for index, dimension in enumerate(dimensions):
        if key_parts[index]:
            continue
        values = available.get(dimension, [])
        # A single-valued dimension doesn't shrink the slice; a huge one (goods
        # codes) would cost more requests than the split can repay.
        if not 1 < len(values) <= MAX_SPLIT_VALUES:
            continue
        saved = 0
        for value in values:
            child = list(key_parts)
            child[index] = value
            saved += _fetch_key_slices(
                entity_id,
                version,
                node_id,
                dimensions,
                child,
                depth + 1,
                csv_gzip,
                done_fragments,
            )
        return saved

    return 0


def fetch_one(node_id: str) -> None:
    entity_id = _SPEC_TO_ENTITY[node_id]
    # Which of the three paths below answers - and, for the sliced ones, what
    # the fragments are named - depends on the version's shape, so a new version
    # can leave fragments of the old one unreferenced-but-live in the manifest
    # (a named-fragment write only replaces its own key). Drop the whole entry
    # first so this fetch defines the asset's complete fragment set. The staged
    # delete only commits if this node succeeds, and the objects it orphans are
    # gc-raw's to collect.
    csv_gzip = entity_id in _CSV_GZIP_RAW
    extension = "csv.gz" if csv_gzip else "parquet"
    run_id = os.environ.get("RUN_ID", "unknown")
    live_fragments = list_raw_fragments(node_id, extension)
    if csv_gzip:
        # The oversized external-trade flow is an incremental fragment set in
        # practice: a GitHub leg can time out after committing hundreds of
        # country slices. Resume from the committed manifest across run ids.
        done_fragments = set(live_fragments)
    else:
        done_fragments = {
            fragment
            for fragment, meta in live_fragments.items()
            if meta.get("run_id") == run_id
        }
    if done_fragments:
        print(f"  -> Resuming {entity_id}: {len(done_fragments):,} fragments already committed")
    else:
        delete_raw_file(node_id, "parquet")
        delete_raw_file(node_id, "csv.gz")

    try:
        version = _latest_version(entity_id)
    except ValueError:
        if entity_id in _RETIRED_HINT:
            _save_retired_marker(entity_id, node_id)
            return
        raise

    url = f"{SDMX_BASE}/data/SSSU,{entity_id},{version}"
    content = _fetch_csv(url)
    if content is not None:
        if _save_sdmx_csv(content, node_id, csv_gzip=csv_gzip):
            return

    saved = 0
    for year in _availability_years(entity_id, version):
        if str(year) in done_fragments:
            saved += 1
            continue
        part_url = f"{url}?startPeriod={year}&endPeriod={year}"
        part = _fetch_csv(part_url)
        if part is None:
            continue
        row_count = _save_sdmx_csv(part, node_id, fragment=str(year), csv_gzip=csv_gzip)
        if row_count:
            done_fragments.add(str(year))
            saved += 1
    if saved:
        return

    dimensions = _dimension_order(entity_id, version)
    saved = _fetch_key_slices(
        entity_id,
        version,
        node_id,
        dimensions,
        [""] * len(dimensions),
        0,
        csv_gzip,
        done_fragments,
    )
    if saved == 0:
        raise ValueError(
            f"{entity_id}: no SDMX-CSV rows returned by full, yearly or key-sliced requests"
        )


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{entity_id.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for entity_id in ENTITY_IDS
]
