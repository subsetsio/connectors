"""GEOGLAM Crop Monitor connector.

Source: the public ArcGIS FeatureServer at data.cropmonitor.org
(CMET/Global_SHP/FeatureServer). The service holds one layer per assessment
month (Global_Synthesis_YYYYMM); every layer shares the schema
Country/Region/Crop/Conditions/Drivers with ~1000 region-crop polygons each.
The month is encoded in the layer name, not the rows, so we stamp it on.

Shape: stateless full re-pull. The whole corpus is ~48 small layers (~50k
rows total) fetched in one request each, so we re-pull everything every run and
overwrite — late revisions to past months are picked up for free.

TLS note: data.cropmonitor.org serves an incomplete certificate chain (the leaf
is valid for data.cropmonitor.org but the InCommon RSA Server CA 2 intermediate
is not sent). We do NOT disable verification; instead we add that intermediate
(which chains to USERTrust RSA, a trusted root in certifi) to a proper SSL
context and install a fully-verifying httpx client.
"""
import os
import ssl

import certifi
import httpx
import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    http_client,
    save_raw_parquet,
    transient_retry,
)

FEATURE_SERVER = (
    "https://data.cropmonitor.org/arcgis/rest/services/CMET/Global_SHP/FeatureServer"
)
PAGE_SIZE = 2000
MAX_PAGES = 50  # safety ceiling per layer (~1k rows/layer; raise+fail if exceeded)

# InCommon RSA Server CA 2 — the intermediate the server omits. Public cert,
# fetched from http://crt.sectigo.com/InCommonRSAServerCA2.crt; chains to
# USERTrust RSA Certification Authority (in certifi). Including it lets us verify
# the full chain WITHOUT relaxing hostname/cert checks.
INCOMMON_RSA_SERVER_CA2 = """-----BEGIN CERTIFICATE-----
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
-----END CERTIFICATE-----
"""

SCHEMA = pa.schema([
    ("period", pa.string()),      # YYYYMM, from the layer name
    ("country", pa.string()),
    ("region", pa.string()),
    ("crop", pa.string()),
    ("conditions", pa.string()),  # raw classification incl. blank / No Data markers
    ("drivers", pa.string()),
])


def _install_verified_client() -> None:
    """Install a fully-verifying httpx client that also trusts the omitted
    InCommon intermediate. Idempotent; safe to call at the top of a fetch fn."""
    ctx = ssl.create_default_context(cafile=certifi.where())
    ctx.load_verify_locations(cadata=INCOMMON_RSA_SERVER_CA2)
    http_client._client = httpx.Client(
        timeout=int(os.environ.get("HTTP_TIMEOUT", "30")),
        headers={"User-Agent": "subsets-geoglam-crop-monitor/1.0"},
        follow_redirects=True,
        verify=ctx,
    )


@transient_retry()
def _get_json(url: str, **params) -> dict:
    resp = get(url, params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _list_layers() -> list[dict]:
    meta = _get_json(FEATURE_SERVER, f="json")
    return meta.get("layers", [])


def _query_layer(layer_id: int) -> list[dict]:
    """Return every feature's attributes for one monthly layer, paging through
    resultOffset until the server stops flagging exceededTransferLimit."""
    rows, offset = [], 0
    for _ in range(MAX_PAGES):
        j = _get_json(
            f"{FEATURE_SERVER}/{layer_id}/query",
            where="1=1",
            outFields="Country,Region,Crop,Conditions,Drivers",
            returnGeometry="false",
            orderByFields="FID",
            resultOffset=offset,
            resultRecordCount=PAGE_SIZE,
            f="json",
        )
        feats = j.get("features", [])
        rows.extend(f.get("attributes", {}) for f in feats)
        if not j.get("exceededTransferLimit") or not feats:
            return rows
        offset += len(feats)
    raise RuntimeError(
        f"layer {layer_id}: exceeded {MAX_PAGES} pages — source grew past expectations"
    )


def fetch_crop_conditions(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    _install_verified_client()

    rows = []
    for layer in _list_layers():
        name = layer.get("name", "")
        period = name.rsplit("_", 1)[-1]  # Global_Synthesis_YYYYMM -> YYYYMM
        if not (len(period) == 6 and period.isdigit()):
            continue  # skip any non-monthly layer the service might add
        for attrs in _query_layer(layer["id"]):
            rows.append({
                "period": period,
                "country": attrs.get("Country"),
                "region": attrs.get("Region"),
                "crop": attrs.get("Crop"),
                "conditions": attrs.get("Conditions"),
                "drivers": attrs.get("Drivers"),
            })

    if not rows:
        raise RuntimeError("FeatureServer returned no monthly layers / no features")
    table = pa.Table.from_pylist(rows, schema=SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="geoglam-crop-monitor-crop-conditions",
        fn=fetch_crop_conditions,
        kind="download",
    ),
]

# One published long-format Delta table: one row per (month, country, region,
# crop). The raw can carry duplicate (country,region,crop) rows within a month
# (multi-polygon admin units, one assessed + one blank); we normalize the blank
# / No Data / #N/A condition markers to NULL and keep the assessed row per key.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="geoglam-crop-monitor-crop-conditions-transform",
        deps=["geoglam-crop-monitor-crop-conditions"],
        sql="""
            WITH norm AS (
                SELECT
                    CAST(strptime(period || '01', '%Y%m%d') AS DATE) AS month,
                    NULLIF(TRIM(country), '') AS country,
                    NULLIF(TRIM(region), '')  AS region,
                    NULLIF(TRIM(crop), '')    AS crop,
                    CASE
                        WHEN UPPER(TRIM(conditions)) IN ('', 'NO DATA', '#N/A', 'N/A', 'NA')
                            THEN NULL
                        -- unambiguous source spelling errors of 'Favourable'
                        WHEN TRIM(conditions) IN ('Favuorable', 'Favourble')
                            THEN 'Favourable'
                        ELSE TRIM(conditions)
                    END AS condition,
                    CASE
                        WHEN UPPER(TRIM(drivers)) IN ('', 'NO DATA', '#N/A', 'N/A', 'NA')
                        THEN NULL ELSE TRIM(drivers)
                    END AS drivers
                FROM "geoglam-crop-monitor-crop-conditions"
            ),
            ranked AS (
                SELECT *,
                    row_number() OVER (
                        PARTITION BY month, country, region, crop
                        ORDER BY CASE WHEN condition IS NULL THEN 1 ELSE 0 END
                    ) AS rn
                FROM norm
                WHERE country IS NOT NULL
                  AND region IS NOT NULL
                  AND crop IS NOT NULL
                  AND month IS NOT NULL
            )
            SELECT month, country, region, crop, condition, drivers
            FROM ranked
            WHERE rn = 1
        """,
    ),
]
