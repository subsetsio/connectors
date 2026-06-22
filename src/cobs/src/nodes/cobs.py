"""COBS Comet Observation Database connector.

Two subsets, both via the COBS Query REST API (https://cobs.si/api):

- ``cobs-comets``       — the comet catalog (one row per comet) from
  ``comet_list.api`` (full catalog in a single page).
- ``cobs-observations`` — the long-format brightness-observation corpus
  (~288k rows). There is NO bulk full-corpus endpoint — an unfiltered
  ``obs_list.api`` returns error code 300 ("too many objects retrieved"), so
  the corpus is assembled per-comet: enumerate the catalog, then page
  ``obs_list.api?id=<id>`` for each comet and stream the rows out.

Both are stateless full re-pulls: the whole corpus is re-fetched each run and
overwritten downstream. Re-fetches pick up revisions/late corrections for free.
The per-comet sweep is ~2446 requests plus extra pages for high-volume comets;
no incremental watermark is used (the source is small enough to re-pull whole).
"""

import json

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    save_raw_ndjson,
    raw_writer,
)

COMET_LIST_URL = "https://cobs.si/api/comet_list.api"
OBS_LIST_URL = "https://cobs.si/api/obs_list.api"

# Safety ceiling: a single comet paging past this many pages (2500 rows/page)
# signals runaway/source change, not normal data — raise rather than loop forever.
MAX_PAGES_PER_COMET = 200


@transient_retry()
def _fetch_json(url: str, params: dict) -> dict:
    resp = get(url, params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _fetch_comet_list() -> list[dict]:
    data = _fetch_json(COMET_LIST_URL, {"format": "json"})
    objs = data.get("objects") or []
    if not objs:
        raise AssertionError(f"comet_list.api returned no objects: info={data.get('info')}")
    return objs


def fetch_comets(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    objs = _fetch_comet_list()
    save_raw_ndjson(objs, asset)


def _flatten_observation(row: dict, comet_id: int) -> dict:
    """Flatten one obs_list.api JSON record into a flat scalar dict.

    The comet{} sub-object carries no id, so we inject the comet_id we queried.
    Every key is always present (None when absent) so the NDJSON columns stay
    stable across the whole corpus.
    """
    comet = row.get("comet") or {}
    observer = row.get("observer") or {}
    obs_method = row.get("obs_method") or {}
    ref_catalog = row.get("ref_catalog") or {}
    instrument_type = row.get("instrument_type") or {}
    camera_type = row.get("camera_type") or {}
    chip_type = row.get("chip_type") or {}
    software_type = row.get("software_type") or {}
    return {
        "obs_date": row.get("obs_date"),
        "comet_id": comet_id,
        "comet_name": comet.get("name"),
        "comet_fullname": comet.get("fullname"),
        "comet_mpc_name": comet.get("mpc_name"),
        "comet_icq_name": comet.get("icq_name"),
        "obs_type": row.get("type"),
        "observer_icq_name": observer.get("icq_name"),
        "observer_first_name": observer.get("first_name"),
        "observer_last_name": observer.get("last_name"),
        "observer_association": observer.get("association"),
        "observer_country": observer.get("country"),
        "magnitude": row.get("magnitude"),
        "magnitude_error": row.get("magnitude_error"),
        "comet_visibility": row.get("comet_visibility"),
        "obs_method_key": obs_method.get("key"),
        "obs_method_name": obs_method.get("name"),
        "ref_catalog_key": ref_catalog.get("key"),
        "instrument_aperture": row.get("instrument_aperture"),
        "instrument_focal_ratio": row.get("instrument_focal_ratio"),
        "instrument_power": row.get("instrument_power"),
        "instrument_type_key": instrument_type.get("key"),
        "coma_diameter": row.get("coma_diameter"),
        "coma_dc": row.get("coma_dc"),
        "tail_length": row.get("tail_length"),
        "tail_length_unit": row.get("tail_length_unit"),
        "tail_pa": row.get("tail_pa"),
        "camera_type_key": camera_type.get("key"),
        "chip_type_key": chip_type.get("key"),
        "software_type_key": software_type.get("key"),
        "icq_reference": row.get("icq_reference"),
        "extinction": row.get("extinction"),
        "integration_time": row.get("integration_time"),
        "date_added": row.get("date_added"),
    }


def fetch_observations(node_id: str) -> None:
    asset = node_id
    comets = _fetch_comet_list()

    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as out:
        for comet in comets:
            cid = comet.get("id")
            if cid is None:
                continue
            page = 1
            pages = 1
            while page <= pages:
                if page > MAX_PAGES_PER_COMET:
                    raise AssertionError(
                        f"comet id={cid} exceeded {MAX_PAGES_PER_COMET} pages — "
                        "likely source change or runaway pagination"
                    )
                data = _fetch_json(
                    OBS_LIST_URL, {"format": "json", "id": cid, "page": page}
                )
                info = data.get("info") or {}
                pages = info.get("pages", 1) or 1
                for row in data.get("objects") or []:
                    out.write(json.dumps(_flatten_observation(row, cid)) + "\n")
                page += 1


DOWNLOAD_SPECS = [
    NodeSpec(id="cobs-comets", fn=fetch_comets, kind="download"),
    NodeSpec(id="cobs-observations", fn=fetch_observations, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="cobs-comets-transform",
        deps=["cobs-comets"],
        sql='''
            SELECT
                CAST(id AS BIGINT)                      AS comet_id,
                type                                    AS comet_type,
                name,
                fullname,
                mpc_name,
                icq_name,
                component,
                TRY_CAST(current_mag AS DOUBLE)         AS current_mag,
                TRY_CAST(perihelion_date AS TIMESTAMP)  AS perihelion_date,
                TRY_CAST(perihelion_mag AS DOUBLE)      AS perihelion_mag,
                TRY_CAST(peak_mag AS DOUBLE)            AS peak_mag,
                TRY_CAST(peak_mag_date AS DATE)         AS peak_mag_date,
                CAST(is_observed AS BOOLEAN)            AS is_observed,
                CAST(is_active AS BOOLEAN)              AS is_active
            FROM "cobs-comets"
            WHERE id IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="cobs-observations-transform",
        deps=["cobs-observations"],
        sql='''
            SELECT
                TRY_CAST(obs_date AS TIMESTAMP)             AS obs_date,
                CAST(comet_id AS BIGINT)                    AS comet_id,
                comet_name,
                comet_fullname,
                comet_mpc_name,
                comet_icq_name,
                obs_type,
                observer_icq_name,
                observer_first_name,
                observer_last_name,
                observer_association,
                observer_country,
                TRY_CAST(magnitude AS DOUBLE)              AS magnitude,
                TRY_CAST(magnitude_error AS DOUBLE)        AS magnitude_error,
                comet_visibility,
                obs_method_key,
                obs_method_name,
                ref_catalog_key,
                TRY_CAST(instrument_aperture AS DOUBLE)    AS instrument_aperture,
                TRY_CAST(instrument_focal_ratio AS DOUBLE) AS instrument_focal_ratio,
                TRY_CAST(instrument_power AS DOUBLE)       AS instrument_power,
                instrument_type_key,
                TRY_CAST(coma_diameter AS DOUBLE)          AS coma_diameter,
                TRY_CAST(coma_dc AS DOUBLE)                AS coma_dc,
                TRY_CAST(tail_length AS DOUBLE)            AS tail_length,
                tail_length_unit,
                TRY_CAST(tail_pa AS DOUBLE)                AS tail_pa,
                camera_type_key,
                chip_type_key,
                software_type_key,
                icq_reference,
                extinction,
                TRY_CAST(integration_time AS DOUBLE)       AS integration_time,
                TRY_CAST(date_added AS TIMESTAMP)          AS date_added
            FROM "cobs-observations"
            WHERE obs_date IS NOT NULL AND comet_id IS NOT NULL
        ''',
    ),
]
