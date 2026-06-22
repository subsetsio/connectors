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
    SqlNodeSpec,
    get,
    post,
    save_raw_ndjson,
    transient_retry,
)
from constants import ENTITY_IDS, REPORT_KEYS

SLUG = "suez-canal-authority"
PBI_BASE = "https://wabi-europe-north-b-api.analysis.windows.net/public/reports"
RESOURCE_HEADER = "X-PowerBI-ResourceKey"
WINDOW = 30000  # querydata row cap per request; reports are far smaller


@transient_retry()
def _get_json(url, key):
    resp = get(url, headers={RESOURCE_HEADER: key}, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


@transient_retry()
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

    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]


# --- Transforms: one published Delta table per report ----------------------
# Each SQL parses/casts the faithful raw rows and, where the source stores
# sub-component rows, sums them to the published grain (GROUP BY visible dims).
# View name == download id (dashes -> must be quoted).

_M = f"{SLUG}-01-monthly-number-net-ton-by-ship-type"
_FY = f"{SLUG}-02-fiscal-year-statistical"
_Y = f"{SLUG}-03-yearly-statistics"
_CD = f"{SLUG}-04-yearly-cargo-ton-by-direction"
_Q = f"{SLUG}-05-yealy-cargo-ton-by-region"
_RG = f"{SLUG}-06-yealy-cargo-ton-by-region-cont"
_CT = f"{SLUG}-07-yearly-cargo-ton-by-cargo-type"

_SQL = {
    _M: f'''
        SELECT
            make_date(CAST(year AS INTEGER), CAST("Month" AS INTEGER), 1) AS date,
            CAST(year AS INTEGER)              AS year,
            CAST("Month" AS INTEGER)           AS month,
            "Ship Type"                        AS ship_type,
            "Direction"                        AS direction,
            "State"                            AS cargo_state,
            CAST(SUM(GREATEST(TRY_CAST("No" AS BIGINT), 0)) AS BIGINT) AS num_vessels,
            SUM(GREATEST(TRY_CAST("NetTonnage" AS DOUBLE), 0)) AS net_tonnage
        FROM "{_M}"
        WHERE year IS NOT NULL AND "Ship Type" IS NOT NULL
        GROUP BY 1, 2, 3, 4, 5, 6
    ''',
    _FY: f'''
        SELECT
            "Fiscal Year"                          AS fiscal_year,
            TRY_CAST("No ( Vessel )" AS BIGINT)    AS num_vessels,
            TRY_CAST("Net Ton" AS DOUBLE)          AS net_ton,
            TRY_CAST("Cargo Ton" AS DOUBLE)        AS cargo_ton,
            TRY_CAST("Tolls (Million $ )" AS DOUBLE)     AS tolls_million_usd,
            TRY_CAST("Tolls (Million L.E. )" AS DOUBLE)  AS tolls_million_egp
        FROM "{_FY}"
        WHERE "Fiscal Year" IS NOT NULL
    ''',
    _Y: f'''
        SELECT
            CAST("Year" AS INTEGER)                AS year,
            TRY_CAST("No ( Vessel )" AS BIGINT)    AS num_vessels,
            TRY_CAST("Net Ton" AS DOUBLE)          AS net_ton,
            TRY_CAST("Cargo Ton" AS DOUBLE)        AS cargo_ton,
            TRY_CAST("Tolls (Million $ )" AS DOUBLE)     AS tolls_million_usd,
            TRY_CAST("Tolls (Million L.E. )" AS DOUBLE)  AS tolls_million_egp
        FROM "{_Y}"
        WHERE "Year" IS NOT NULL
    ''',
    _CD: f'''
        SELECT
            CAST("Year" AS INTEGER)         AS year,
            "Direction"                     AS direction,
            TRY_CAST("Cargo Ton" AS DOUBLE) AS cargo_ton
        FROM "{_CD}"
        WHERE "Year" IS NOT NULL
    ''',
    _Q: f'''
        SELECT
            CAST(year AS INTEGER)              AS year,
            CAST("Quarter" AS INTEGER)         AS quarter,
            "CategoryName_en"                  AS ship_type,
            "Port"                             AS direction,
            CAST(SUM(GREATEST(TRY_CAST("No" AS BIGINT), 0)) AS BIGINT) AS num_vessels,
            SUM(GREATEST(TRY_CAST("NetTonnage" AS DOUBLE), 0)) AS net_tonnage
        FROM "{_Q}"
        WHERE year IS NOT NULL AND "CategoryName_en" IS NOT NULL
        GROUP BY 1, 2, 3, 4
    ''',
    _RG: f'''
        SELECT
            CAST(year AS INTEGER)                  AS year,
            "Region"                               AS region,
            "Region_Code"                          AS region_code,
            "Direction"                            AS direction,
            "Terminal"                             AS terminal,
            SUM(GREATEST(TRY_CAST("CargoTonnage" AS DOUBLE), 0)) AS cargo_tonnage
        FROM "{_RG}"
        WHERE year IS NOT NULL AND "Region" IS NOT NULL
        GROUP BY 1, 2, 3, 4, 5
    ''',
    _CT: f'''
        SELECT
            CAST("Year" AS INTEGER)                AS year,
            "CargoType"                            AS cargo_type,
            "Goods"                                AS cargo_group,
            "Direction"                            AS direction,
            SUM(GREATEST(TRY_CAST("CargoTonnage" AS DOUBLE), 0)) AS cargo_tonnage
        FROM "{_CT}"
        WHERE "Year" IS NOT NULL AND "CargoType" IS NOT NULL
        GROUP BY 1, 2, 3, 4
    ''',
}

TRANSFORM_SPECS = [
    SqlNodeSpec(id=f"{s.id}-transform", deps=[s.id], sql=_SQL[s.id])
    for s in DOWNLOAD_SPECS
]
