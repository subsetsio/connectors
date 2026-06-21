"""JPL Solar System Dynamics / CNEOS REST JSON.

cad/fireball use the {fields[], data[][]} envelope; sentry/nhats return lists of
dicts. All small enough for in-memory ndjson. cad is the only date-windowed
endpoint and we pull its whole history with a fixed wide window.
"""

from __future__ import annotations

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson
from utils import get_json

# JPL endpoint -> request params (cad needs an explicit wide history window;
# the others return their full snapshot with no params).
JPL_ENDPOINTS = {
    "cad": {"date-min": "1900-01-01", "date-max": "2100-01-01"},
    "fireball": {},
    "sentry": {},
    "nhats": {},
}


def fetch_jpl(node_id: str) -> None:
    asset = node_id
    endpoint = node_id[len("nasa-"):]
    params = JPL_ENDPOINTS[endpoint]
    payload = get_json(f"https://ssd-api.jpl.nasa.gov/{endpoint}.api", params)

    data = payload.get("data") or []
    fields = payload.get("fields")
    if isinstance(fields, list) and data and isinstance(data[0], list):
        # {fields[], data[][]} envelope (cad, fireball). Sanitize dashed names.
        cols = [f.replace("-", "_") for f in fields]
        records = [dict(zip(cols, row)) for row in data]
    else:
        # list of dicts (sentry, nhats)
        records = list(data)

    # Flatten any one-level nested dicts (nhats min_dv / min_dur) so the raw is
    # flat scalars and the transform needs no struct access.
    flat = []
    for rec in records:
        out = {}
        for k, v in rec.items():
            if isinstance(v, dict):
                for kk, vv in v.items():
                    out[f"{k}_{kk}"] = vv
            else:
                out[k] = v
        flat.append(out)

    if not flat:
        raise AssertionError(f"{asset}: JPL {endpoint} returned no rows")
    save_raw_ndjson(flat, asset)


# Cast the string-typed envelope/dict values to real numerics (TRY_CAST so odd/
# empty cells become NULL rather than failing the node).
_JPL_SQL = {
    "nasa-cad": '''
        SELECT des, orbit_id,
               TRY_CAST(jd AS DOUBLE)        AS jd,
               cd,
               TRY_CAST(dist AS DOUBLE)      AS dist_au,
               TRY_CAST(dist_min AS DOUBLE)  AS dist_min_au,
               TRY_CAST(dist_max AS DOUBLE)  AS dist_max_au,
               TRY_CAST(v_rel AS DOUBLE)     AS v_rel_kms,
               TRY_CAST(v_inf AS DOUBLE)     AS v_inf_kms,
               t_sigma_f,
               TRY_CAST(h AS DOUBLE)         AS h_mag
        FROM "nasa-cad"
    ''',
    "nasa-fireball": '''
        SELECT TRY_CAST(date AS TIMESTAMP)    AS event_time,
               TRY_CAST(energy AS DOUBLE)     AS energy_kt,
               TRY_CAST(impact_e AS DOUBLE)   AS impact_energy_kt,
               TRY_CAST(lat AS DOUBLE)        AS lat,
               lat_dir,
               TRY_CAST(lon AS DOUBLE)        AS lon,
               lon_dir,
               TRY_CAST(alt AS DOUBLE)        AS altitude_km,
               TRY_CAST(vel AS DOUBLE)        AS velocity_kms
        FROM "nasa-fireball"
        WHERE date IS NOT NULL
    ''',
    "nasa-sentry": '''
        SELECT des, id, fullname,
               TRY_CAST(h AS DOUBLE)          AS h_mag,
               TRY_CAST(diameter AS DOUBLE)   AS diameter_km,
               TRY_CAST(v_inf AS DOUBLE)      AS v_inf_kms,
               TRY_CAST(ps_cum AS DOUBLE)     AS palermo_scale_cum,
               TRY_CAST(ps_max AS DOUBLE)     AS palermo_scale_max,
               TRY_CAST(ts_max AS DOUBLE)     AS torino_scale_max,
               TRY_CAST(ip AS DOUBLE)         AS impact_prob,
               TRY_CAST(n_imp AS BIGINT)      AS n_impacts,
               "range"                        AS year_range,
               last_obs,
               TRY_CAST(last_obs_jd AS DOUBLE) AS last_obs_jd
        FROM "nasa-sentry"
    ''',
    "nasa-nhats": '''
        SELECT des, fullname, orbit_id,
               TRY_CAST(h AS DOUBLE)          AS h_mag,
               TRY_CAST(min_size AS DOUBLE)   AS min_size_m,
               TRY_CAST(max_size AS DOUBLE)   AS max_size_m,
               TRY_CAST(min_dv_dv AS DOUBLE)  AS min_dv_kms,
               TRY_CAST(min_dv_dur AS BIGINT) AS min_dv_duration_days,
               TRY_CAST(min_dur_dv AS DOUBLE) AS min_dur_dv_kms,
               TRY_CAST(min_dur_dur AS BIGINT) AS min_dur_days,
               TRY_CAST(n_via_traj AS BIGINT) AS n_trajectories,
               obs_start, obs_end, obs_flag,
               TRY_CAST(obs_mag AS DOUBLE)    AS obs_mag
        FROM "nasa-nhats"
    ''',
}


DOWNLOAD_SPECS = [
    NodeSpec(id=f"nasa-{e}", fn=fetch_jpl, kind="download") for e in JPL_ENDPOINTS
]

TRANSFORM_SPECS = [
    SqlNodeSpec(id=f"{s.id}-transform", deps=[s.id], sql=_JPL_SQL[s.id])
    for s in DOWNLOAD_SPECS
]
