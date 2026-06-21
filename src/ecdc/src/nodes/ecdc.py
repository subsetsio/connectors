"""ECDC Surveillance Atlas of Infectious Diseases connector.

Source: the ECDC Atlas REST service (https://atlas.ecdc.europa.eu/public/AtlasService/rest),
which exposes TESSy-sourced EU/EEA infectious-disease surveillance data. Each
published subset is one (health topic x live CURRENT dataset) pair -- i.e. one
disease's surveillance table.

Fetch strategy (stateless full re-pull -- shape 1):
The CURRENT.* datasets are overwritten in place by ECDC each release with no
incremental filter, so every run re-fetches the full table per entity and
overwrites. No watermark / cursor / state.

For each entity we know its (healthTopicId, datasetId, native_time_unit) from
collect (inlined in ENTITY_META). The export's geoLevel and timeUnit are NOT
fixed -- they vary per dataset (yearly diseases publish at geoLevel=2/Year;
influenza & RSV at geoLevel=1/Week). A dataset often *also* exposes coarser or
finer re-cuts of the same data (e.g. a yearly dataset re-aggregated by Month, or
country data also offered at a subnational geoLevel). We publish exactly ONE
resolution per subset -- the dataset's native time unit at its country-level
geoLevel -- because (a) the re-cuts are redundant aggregations of the same
underlying counts, and (b) the heavy sub-year re-cuts of large datasets (e.g.
salmonellosis serotype data at Month granularity is tens of millions of rows)
time the export server out with 504s. We discover the available resolutions per
entity from GetIndicatorMeasuresForHealthTopicAndDataset, pick the native one,
fetch its full CSV via GetMeasuresResultsExportFile, and stream it to parquet so
the few very large tables (salmonellosis ~2.5M rows) stay within memory.
"""

import csv
import io

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    raw_parquet_writer,
    transient_retry,
)

BASE = "https://atlas.ecdc.europa.eu/public/AtlasService/rest"

# Rows per streamed parquet row-group / from_pylist batch.
BATCH_ROWS = 50_000

# Finest-first ordering used only when an entity's native time unit is unknown.
_UNIT_ORDER = {"Week": 0, "Month": 1, "Year": 2}

# (healthTopicId, datasetId, native_time_unit) per entity -- the entity union,
# copied from data/sources/ecdc/work/entity_union.json joined to collect's
# source_metadata (native unit derived from the dataset mnemonic granularity).
ENTITY_META = {
    "amr-current-amr-yearly": (4, 354, "Year"),
    "anth-current-fwd-yearly": (5, 347, "Year"),
    "botu-current-fwd-yearly": (7, 347, "Year"),
    "bruc-current-fwd-yearly": (8, 347, "Year"),
    "camp-current-fwd-amr-yearly": (9, 1296, "Year"),
    "camp-current-fwd-yearly": (9, 347, "Year"),
    "cchf-current-evd-yearly": (10, 438, "Year"),
    "chik-current-evd-yearly": (11, 438, "Year"),
    "chlam-current-sti-yearly": (12, 464, "Year"),
    "chol-current-fwd-yearly": (13, 347, "Year"),
    "consyph-current-sti-yearly": (14, 464, "Year"),
    "cryp-current-fwd-yearly": (15, 347, "Year"),
    "dengue-current-evd-yearly": (16, 438, "Year"),
    "echi-current-fwd-yearly": (18, 347, "Year"),
    "filo-current-evd-yearly": (19, 438, "Year"),
    "giar-current-fwd-yearly": (20, 347, "Year"),
    "gono-current-sti-yearly": (21, 464, "Year"),
    "haeinf-current-ibd-yearly": (22, 423, "Year"),
    "haicdi-current-haicdi-yearly": (78, 901, "Year"),
    "haiicu-current-haiicu-yearly": (79, 475, "Year"),
    "haissi-current-haissi-yearly": (77, 558, "Year"),
    "hanta-current-evd-yearly": (24, 438, "Year"),
    "hepa-current-fwd-yearly": (25, 347, "Year"),
    "hepb-current-hepbc-yearly": (26, 361, "Year"),
    "hepc-current-hepbc-yearly": (27, 361, "Year"),
    "hivaids-current-hivaids-yearly": (75, 881, "Year"),
    "infl-current-infl-flunews": (29, 330, None),
    "infl-current-infl-weekly": (29, 289, "Week"),
    "legi-current-legi-yearly": (30, 519, "Year"),
    "lept-current-fwd-yearly": (31, 347, "Year"),
    "lgv-current-sti-yearly": (32, 464, "Year"),
    "list-current-fwd-yearly": (33, 347, "Year"),
    "lymeneuro-current-evd-yearly": (76, 438, "Year"),
    "mala-current-evd-yearly": (34, 438, "Year"),
    "meas-current-measrube-monthly": (35, 335, "Month"),
    "meni-current-ibd-yearly": (36, 423, "Year"),
    "mump-current-vpd-yearly": (37, 421, "Year"),
    "pert-current-vpd-yearly": (38, 421, "Year"),
    "plag-current-evd-yearly": (39, 438, "Year"),
    "pneu-current-ibd-yearly": (40, 423, "Year"),
    "qfev-current-evd-yearly": (42, 438, "Year"),
    "rabi-current-evd-yearly": (43, 438, "Year"),
    "rsv-current-infl-weekly": (74, 289, "Week"),
    "rube-current-measrube-monthly": (45, 335, "Month"),
    "salm-current-fwd-amr-yearly": (46, 1296, "Year"),
    "salm-current-fwd-yearly": (46, 347, "Year"),
    "shig-current-fwd-amr-yearly": (48, 1296, "Year"),
    "shig-current-fwd-yearly": (48, 347, "Year"),
    "stec-current-fwd-yearly": (59, 347, "Year"),
    "syph-current-sti-yearly": (50, 464, "Year"),
    "tbe-current-evd-yearly": (56, 438, "Year"),
    "teta-current-vpd-yearly": (51, 421, "Year"),
    "toxo-current-fwd-yearly": (52, 347, "Year"),
    "tric-current-fwd-yearly": (53, 347, "Year"),
    "tube-current-tube-yearly": (54, 419, "Year"),
    "tula-current-evd-yearly": (55, 438, "Year"),
    "vcjd-current-fwd-yearly": (57, 347, "Year"),
    "wnf-current-evd-yearly": (60, 438, "Year"),
    "wnf-current-wnf-weekly": (60, 138, "Week"),
    "yelf-current-evd-yearly": (61, 438, "Year"),
    "yers-current-fwd-yearly": (62, 347, "Year"),
    "zika-current-evd-yearly": (70, 438, "Year"),
    "zika-current-zikv-weekly": (70, 284, "Week"),
}

SCHEMA = pa.schema([
    ("health_topic", pa.string()),
    ("population", pa.string()),
    ("indicator", pa.string()),
    ("unit", pa.string()),
    ("geo_level", pa.string()),
    ("time_unit", pa.string()),
    ("time", pa.string()),
    ("region_code", pa.string()),
    ("region_name", pa.string()),
    ("num_value", pa.float64()),
    ("txt_value", pa.string()),
])


@transient_retry()
def _get_json(url: str, params: dict) -> dict:
    resp = get(url, params=params, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.json()


@transient_retry()
def _get_text(url: str, params: dict) -> str:
    resp = get(url, params=params, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.text


def _resolutions(health_topic_id: int, dataset_id: int) -> list[tuple[str, str]]:
    """Distinct (geoLevelNumber, timeUnitLabel) the source publishes for this
    (topic, dataset), gathered across all of its indicator measures."""
    data = _get_json(
        f"{BASE}/GetIndicatorMeasuresForHealthTopicAndDataset",
        {"healthTopicId": health_topic_id, "datasetId": dataset_id},
    )
    seen = set()
    for measure in data.get("Measures") or []:
        rlist = (measure.get("ResolutionList") or {}).get("Resolutions") or []
        for r in rlist:
            geo = r.get("GeoLevelNumber")
            unit = r.get("TimeUnitLabel")
            if geo is not None and unit:
                seen.add((str(geo), str(unit)))
    return sorted(seen)


def _pick_resolution(resolutions, native_unit):
    """One (geoLevel, timeUnit) to publish: the dataset's native time unit
    (falling back to the finest available when unknown), at its country-level
    geoLevel (the smallest geoLevel number available for that unit)."""
    units = {u for _, u in resolutions}
    if native_unit in units:
        unit = native_unit
    else:
        unit = min(units, key=lambda u: _UNIT_ORDER.get(u, 9))
    geo = min((g for g, u in resolutions if u == unit), key=int)
    return geo, unit


def _parse_num(raw: str):
    raw = (raw or "").strip()
    if raw in ("", "-"):
        return None
    try:
        return float(raw)
    except ValueError:
        return None


def _export_rows(health_topic_id: int, dataset_id: int, geo_level: str, time_unit: str):
    """Full CSV export for one resolution, yielded as schema-shaped dicts."""
    text = _get_text(
        f"{BASE}/GetMeasuresResultsExportFile",
        {
            "healthTopicId": health_topic_id,
            "datasetId": dataset_id,
            "measurePopulation": "",
            "measureIds": "",
            "measureTypes": "I,Q",
            "timeCodes": "",
            "geoCodes": "",
            "geoLevel": geo_level,
            "timeUnit": time_unit,
        },
    )
    reader = csv.DictReader(io.StringIO(text))
    for row in reader:
        txt = (row.get("TxtValue") or "").strip()
        if txt in ("", "None"):
            txt = None
        yield {
            "health_topic": row.get("HealthTopic"),
            "population": row.get("Population"),
            "indicator": row.get("Indicator"),
            "unit": row.get("Unit"),
            "geo_level": geo_level,
            "time_unit": time_unit,
            "time": row.get("Time"),
            "region_code": row.get("RegionCode"),
            "region_name": row.get("RegionName"),
            "num_value": _parse_num(row.get("NumValue")),
            "txt_value": txt,
        }


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    entity_id = node_id[len("ecdc-"):]
    health_topic_id, dataset_id, native_unit = ENTITY_META[entity_id]

    resolutions = _resolutions(health_topic_id, dataset_id)
    if not resolutions:
        # Every union entity had a resolution at authoring time; an empty set
        # now means the catalog shifted under us -- fail loudly rather than
        # publishing an empty table.
        raise AssertionError(
            f"{asset}: no resolutions for healthTopicId={health_topic_id} "
            f"datasetId={dataset_id}"
        )

    geo_level, time_unit = _pick_resolution(resolutions, native_unit)

    # Stream the (possibly multi-million-row) CSV to parquet in batches so the
    # large serotype-level foodborne tables stay within memory.
    with raw_parquet_writer(asset, SCHEMA) as writer:
        batch = []
        for row in _export_rows(health_topic_id, dataset_id, geo_level, time_unit):
            batch.append(row)
            if len(batch) >= BATCH_ROWS:
                writer.write_table(pa.Table.from_pylist(batch, schema=SCHEMA))
                batch = []
        if batch:
            writer.write_table(pa.Table.from_pylist(batch, schema=SCHEMA))


DOWNLOAD_SPECS = [
    NodeSpec(id=f"ecdc-{eid.lower().replace('_', '-')}", fn=fetch_one, kind="download")
    for eid in ENTITY_META
]

# One published Delta table per subset: parse-and-type pass, drop fully-missing
# rows (both num_value and txt_value null), de-duplicate on the natural grain.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT DISTINCT
                health_topic,
                population,
                indicator,
                unit,
                geo_level,
                time_unit,
                time,
                region_code,
                region_name,
                CAST(num_value AS DOUBLE) AS num_value,
                txt_value
            FROM "{s.id}"
            WHERE num_value IS NOT NULL OR txt_value IS NOT NULL
        ''',
    )
    for s in DOWNLOAD_SPECS
]
