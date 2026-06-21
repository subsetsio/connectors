"""Four UNSD SDMX 2.1 dataflows on data.un.org.

One parametric fetcher: each dataflow is fetched whole as SDMX-CSV
(Accept: application/vnd.sdmx.data+csv). Raw -> csv file, read directly by the
transform. The two energy flows are ~84-136MB; downloaded in one shot. The API
supports no modified-since delta filter, so every refresh re-pulls the full flow.
"""
from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_file,
    transient_retry,
)

SDMX_BASE = "https://data.un.org/WS/rest/data/UNSD"
SDMX_CSV = "application/vnd.sdmx.data+csv;version=1.0.0"

# Case-sensitive SDMX dataflow ids (the API rejects a wrong case). Keyed by the
# lowered node-id suffix so fetch_sdmx can recover the real id from its node id.
SDMX_FLOWS = {
    "df-undata-countrydata": "DF_UNDATA_COUNTRYDATA",
    "df-undata-energy": "DF_UNDATA_ENERGY",
    "df-undata-energybalance": "DF_UNData_EnergyBalance",
    "df-undata-unfcc": "DF_UNData_UNFCC",
}


@transient_retry()
def _get_text(url, headers=None):
    resp = get(url, headers=headers, timeout=(10.0, 600.0))
    resp.raise_for_status()
    return resp.text


def fetch_sdmx(node_id: str) -> None:
    """Fetch one UNSD SDMX dataflow whole as SDMX-CSV; save the csv verbatim."""
    asset = node_id
    suffix = node_id[len("un-statistics-division-"):]
    flow = SDMX_FLOWS.get(suffix)
    if flow is None:
        raise AssertionError(f"{asset}: no SDMX dataflow mapped for suffix '{suffix}'")
    text = _get_text(f"{SDMX_BASE},{flow}/", headers={"Accept": SDMX_CSV})
    if text.count("\n") < 2:
        raise AssertionError(f"{asset}: SDMX-CSV for {flow} has no data rows")
    save_raw_file(text, asset, extension="csv")


DOWNLOAD_SPECS = [
    NodeSpec(id="un-statistics-division-df-undata-countrydata", fn=fetch_sdmx, kind="download"),
    NodeSpec(id="un-statistics-division-df-undata-energy", fn=fetch_sdmx, kind="download"),
    NodeSpec(id="un-statistics-division-df-undata-energybalance", fn=fetch_sdmx, kind="download"),
    NodeSpec(id="un-statistics-division-df-undata-unfcc", fn=fetch_sdmx, kind="download"),
]


# SDMX flows share the same generic shape: keep every dimension column, type the
# observation value, drop rows with no numeric value. DATAFLOW is redundant.
def _sdmx_transform(download_id: str) -> SqlNodeSpec:
    return SqlNodeSpec(
        id=f"{download_id}-transform",
        deps=[download_id],
        sql=f'''
            SELECT * EXCLUDE (OBS_VALUE, DATAFLOW),
                   TRY_CAST(OBS_VALUE AS DOUBLE) AS obs_value
            FROM "{download_id}"
            WHERE TRY_CAST(OBS_VALUE AS DOUBLE) IS NOT NULL
        ''',
    )


TRANSFORM_SPECS = [
    _sdmx_transform("un-statistics-division-df-undata-countrydata"),
    _sdmx_transform("un-statistics-division-df-undata-energy"),
    _sdmx_transform("un-statistics-division-df-undata-energybalance"),
    _sdmx_transform("un-statistics-division-df-undata-unfcc"),
]
