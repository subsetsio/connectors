"""NY Fed — primary dealer statistics (one full-history series per keyid)."""

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_ndjson, transient_retry
from utils import BASE, get_json


@transient_retry()
def _get_series(keyid: str):
    resp = get(f"{BASE}/pd/get/{keyid}.json", timeout=(10.0, 120.0))
    if resp.status_code == 404:
        return None  # permanent: series id no longer served, skip it
    resp.raise_for_status()
    return resp.json().get("pd", {}).get("timeseries", [])


def _pd_rows():
    listing = get_json("pd/list/timeseries.json").get("pd", {}).get("timeseries", [])
    meta = {}
    for s in listing:
        kid = s.get("keyid")
        if kid and kid not in meta:
            meta[kid] = {"seriesbreak": s.get("seriesbreak"),
                         "description": s.get("description")}
    for keyid, info in meta.items():
        series = _get_series(keyid)
        if not series:
            continue
        for obs in series:
            yield {
                "asofdate": obs.get("asofdate"),
                "keyid": obs.get("keyid") or keyid,
                "value": obs.get("value"),
                "seriesbreak": info["seriesbreak"],
                "description": info["description"],
            }


def fetch_primary_dealer_values(node_id: str) -> None:
    # Generator keeps memory bounded across ~1500 series.
    save_raw_ndjson(_pd_rows(), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="ny-fed-primary-dealer-values", fn=fetch_primary_dealer_values, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="ny-fed-primary-dealer-values-transform",
        deps=["ny-fed-primary-dealer-values"],
        sql='''
            SELECT
                TRY_CAST(asofdate AS DATE)           AS week_ending,
                keyid                                AS series_id,
                seriesbreak                          AS series_break,
                description                          AS series_description,
                TRY_CAST(value AS DOUBLE)            AS value_millions
            FROM "ny-fed-primary-dealer-values"
            WHERE TRY_CAST(asofdate AS DATE) IS NOT NULL
              AND TRY_CAST(value AS DOUBLE) IS NOT NULL
        ''',
    ),
]
