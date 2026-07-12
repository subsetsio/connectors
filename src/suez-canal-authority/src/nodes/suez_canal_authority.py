"""Suez Canal Authority — navigation statistics.

The SCA publishes its navigation statistics as 7 anonymous Power BI "publish to
web" reports embedded on
https://www.suezcanal.gov.eg/English/Navigation/Pages/NavigationStatistics.aspx
Each report is a small tabular model queryable via the public Power BI querydata
endpoint with an anonymous resource key (no login). One download spec per report.

Fetch shape: **stateless full re-pull** (shape 1). Each report is tiny (tens to a
few thousand rows) and exposes no incremental/since filter, so we re-query the
whole model every run and overwrite. For each report we:
  1. GET  /public/reports/{key}/modelsAndExploration  -> modelId, datasetId, reportId
  2. POST /public/reports/conceptualschema            -> entity name + columns
  3. POST /public/reports/querydata                   -> rows (compressed DSR)
then decode the DSR (ValueDicts + R repeat-bitmask + Ø null-bitmask) into flat
records and save NDJSON. Numeric-looking values from non-categorical columns are
coerced to int/float so types are stable across rows (one report ships a toll
value as a stringified float); categorical (dictionary-encoded) values stay text.

The raw asset is the faithful component-level table. Several reports (05/06/07)
store sub-component rows that the source's own pivotTable SUMs to the published
figure, so the SQL transform aggregates (GROUP BY the visible dimensions,
SUM the metric) — the same reduction the SCA report displays.
"""

from subsets_utils import (
    NodeSpec,
    get,
    post,
    save_raw_parquet,
)
import pyarrow as pa
from constants import ENTITY_IDS, REPORT_KEYS

SLUG = "suez-canal-authority"
PBI_BASE = "https://wabi-europe-north-b-api.analysis.windows.net/public/reports"
RESOURCE_HEADER = "X-PowerBI-ResourceKey"
WINDOW = 30000  # querydata row cap per request; reports are far smaller


def _get_json(url, key):
    resp = get(url, headers={RESOURCE_HEADER: key}, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _post_json(url, key, payload):
    resp = post(url, headers={RESOURCE_HEADER: key}, json=payload, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _coerce(value, is_categorical):
    """Stabilise types: leave dictionary-encoded categoricals as text, parse
    numeric strings from value columns into int/float, keep nulls as None."""
    if value is None or is_categorical:
        return value
    if isinstance(value, (int, float)):
        return value
    text = str(value).strip()
    try:
        number = float(text)
    except ValueError:
        return text
    return int(number) if number.is_integer() else number


def _decode_dsr(data):
    """Decode one Power BI querydata DSR result into a list of flat dict rows.

    Each row's 'C' array omits leading values that repeat from the previous row
    (the 'R' repeat-bitmask) and values that are null (the 'Ø' null-bitmask);
    dictionary-encoded string columns carry an integer index into ValueDicts.
    """
    ds = data["dsr"]["DS"][0]
    value_dicts = ds.get("ValueDicts", {})
    dm0 = ds["PH"][0]["DM0"]
    if not dm0:
        return []

    descriptor = dm0[0]["S"]  # ordered column schema, only on the first row
    ncols = len(descriptor)
    dict_names = [col.get("DN") for col in descriptor]

    # Map each "Gn" group token to its source property name.
    gn_to_prop = {}
    for sel in data["descriptor"]["Select"]:
        group_keys = sel.get("GroupKeys")
        if group_keys:
            prop = group_keys[0]["Source"]["Property"]
        else:
            prop = sel.get("Name", "").split(".")[-1]
        gn_to_prop[sel["Value"]] = prop
    colnames = [gn_to_prop.get(col["N"], col["N"]) for col in descriptor]

    prev = [None] * ncols
    rows = []
    for item in dm0:
        compressed = item.get("C", [])
        repeat_mask = item.get("R", 0)
        null_mask = item.get("Ø", 0)
        ci = 0
        row = [None] * ncols
        for i in range(ncols):
            if null_mask & (1 << i):
                row[i] = None
            elif repeat_mask & (1 << i):
                row[i] = prev[i]
            else:
                row[i] = compressed[ci]
                ci += 1
        prev = list(row)

        record = {}
        for i in range(ncols):
            value = row[i]
            is_categorical = dict_names[i] is not None
            if is_categorical and isinstance(value, int):
                value = value_dicts[dict_names[i]][value]
            record[colnames[i]] = _coerce(value, is_categorical)
        rows.append(record)
    return rows


def _arrow_type(values):
    non_null = [v for v in values if v is not None]
    if not non_null:
        return pa.string()
    if all(isinstance(v, bool) for v in non_null):
        return pa.bool_()
    if all(isinstance(v, int) and not isinstance(v, bool) for v in non_null):
        return pa.int64()
    if all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in non_null):
        return pa.float64()
    return pa.string()


def _to_arrow_table(rows):
    columns = list(rows[0].keys())
    fields = []
    arrays = []
    for col in columns:
        values = [row.get(col) for row in rows]
        typ = _arrow_type(values)
        if pa.types.is_string(typ):
            values = [None if v is None else str(v) for v in values]
        elif pa.types.is_floating(typ):
            values = [None if v is None else float(v) for v in values]
        fields.append(pa.field(col, typ))
        arrays.append(pa.array(values, type=typ))
    return pa.Table.from_arrays(arrays, schema=pa.schema(fields))


def fetch_one(node_id: str) -> None:
    asset = node_id  # the spec id IS the asset name
    entity_id = node_id[len(SLUG) + 1:]
    key = REPORT_KEYS[entity_id]

    meta = _get_json(f"{PBI_BASE}/{key}/modelsAndExploration?preferReadOnlySession=true", key)
    model = meta["models"][0]
    model_id = model["id"]
    dataset_id = model["dbName"]
    report_id = meta["exploration"]["reportId"]

    schema = _post_json(
        f"{PBI_BASE}/conceptualschema", key,
        {"modelIds": [model_id], "userPreferredLocale": "en-US"},
    )
    user_entities = [
        e for sch in schema.get("schemas", [])
        for e in sch["schema"].get("Entities", [])
        if not e.get("Private")
    ]
    if not user_entities:
        raise AssertionError(f"{asset}: conceptualschema returned no user entity")
    entity = user_entities[0]
    entity_name = entity["Name"]
    columns = [p["Name"] for p in entity["Properties"]]

    select = [
        {"Column": {"Expression": {"SourceRef": {"Source": "r"}}, "Property": col},
         "Name": f"{entity_name}.{col}"}
        for col in columns
    ]
    payload = {
        "version": "1.0.0",
        "queries": [{
            "Query": {"Commands": [{"SemanticQueryDataShapeCommand": {
                "Query": {
                    "Version": 2,
                    "From": [{"Name": "r", "Entity": entity_name, "Type": 0}],
                    "Select": select,
                },
                "Binding": {
                    "Primary": {"Groupings": [{"Projections": list(range(len(select)))}]},
                    "DataReduction": {"DataVolume": 4, "Primary": {"Window": {"Count": WINDOW}}},
                    "Version": 1,
                },
            }}]},
            "QueryId": "",
            "ApplicationContext": {"DatasetId": dataset_id, "Sources": [{"ReportId": report_id}]},
        }],
        "cancelQueries": [],
        "modelId": model_id,
    }
    result = _post_json(f"{PBI_BASE}/querydata?synchronous=true", key, payload)
    data = result["results"][0]["result"]["data"]

    dsr = data.get("dsr", {})
    shapes = dsr.get("DataShapes")
    if shapes and shapes[0].get("odata.error"):
        err = shapes[0]["odata.error"]
        raise AssertionError(f"{asset}: querydata error {err.get('code')}: "
                             f"{err.get('message', {}).get('value')}")

    rows = _decode_dsr(data)
    if len(rows) >= WINDOW:
        raise AssertionError(f"{asset}: hit querydata window cap {WINDOW}; pagination needed")
    if not rows:
        raise AssertionError(f"{asset}: querydata returned no rows")

    save_raw_parquet(_to_arrow_table(rows), asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]
