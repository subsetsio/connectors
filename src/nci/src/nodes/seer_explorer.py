"""NCI SEER*Explorer — NCI's national cancer-statistics engine.

SEER*Explorer (seer.cancer.gov): its server-side `render_region_5.php` returns
(double-encoded) JSON {info, data}: `info.key-order` names the dimensions
encoded in each `data` key (e.g. "2_1_1_1_1_1"), `info.data-fields` names the
positional columns of each `data_series` row. We fetch one statistic type per
node, iterating every cancer site available for that statistic (discovered from
`render_region_3_controls.php`), broken down by sex, and resolve dimension ids
to labels via `get_var_formats.php`. Stateless full re-pull: the whole corpus is
a few hundred small JSON responses and refreshes annually with the new SEER
submission, so there is no incremental filter to exploit.

Raw is written as NDJSON per node: the column set is stable within a statistic
but differs across statistics (incidence carries year/rate, survival carries
stage/percent, etc.), so a single declared parquet schema does not fit. Each
TRANSFORM_SPEC types its own statistic.
"""
import json

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_ndjson,
    transient_retry,
)

SEER_BASE = (
    "https://seer.cancer.gov/statistics-network/explorer/source/content_writers/"
)

# ---- HTTP with honest retry classification -------------------------------


@transient_retry()
def _get_json(url, **params):
    resp = get(url, params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    body = resp.json()
    # SEER*Explorer endpoints return a JSON-encoded string (double-encoded).
    return json.loads(body) if isinstance(body, str) else body


# ============================ SEER*Explorer ===============================

# slug (entity id minus the "seer-explorer-" prefix) -> fetch configuration.
# graph_type picks the view whose response carries the richest series for that
# statistic; `fixed` pins the non-series dimensions to their "all" value; `loop`
# fans an extra dimension that the view does NOT encode in its data key.
SEER_STATS = {
    "seer-incidence": {
        "data_type": 1,
        "graph_type": 1,  # Long-Term Trends -> rate by year
        "fixed": {"rate_type": 2, "race": 1, "age_range": 1, "subtype": 1},
        "loop": None,
    },
    "us-mortality": {
        "data_type": 2,
        "graph_type": 1,
        "fixed": {"race": 1, "age_range": 1},
        "loop": None,
    },
    "preliminary-incidence-rates": {
        "data_type": 3,
        "graph_type": 1,
        "fixed": {"rate_type": 2, "race": 1, "age_range": 1, "subtype": 1},
        "loop": None,
    },
    "survival": {
        "data_type": 4,
        "graph_type": 5,  # 5-Year Survival (relative survival %)
        "fixed": {"race": 1, "age_range": 1, "stage": 101},
        # survival's data key has no interval dim, so fan it explicitly:
        "loop": ("relative_survival_interval", [1, 2, 3, 5]),
    },
    "prevalence": {
        "data_type": 5,
        "graph_type": 1,
        "fixed": {"age_range": 1},
        "loop": None,
    },
    "risk-of-diagnosis-dying": {
        "data_type": 6,
        "graph_type": 1,
        "fixed": {"race": 1, "age_range": 300},
        "loop": ("stat_type", [10, 11]),  # 10=risk of diagnosis, 11=risk of dying
    },
}

# dimensions we resolve id -> human label from get_var_formats.php
_LABELLED_DIMS = (
    "site",
    "sex",
    "race",
    "age_range",
    "rate_type",
    "stage",
    "subtype",
    "stat_type",
    "relative_survival_interval",
)


def _seer_formats() -> dict:
    return _get_json(SEER_BASE + "get_var_formats.php")["VariableFormats"]


def _seer_sites(data_type: int, graph_type: int) -> list:
    """The cancer sites available for a given statistic, per the source's own
    control endpoint. Raises if the shape changed (no silent under-coverage)."""
    ctrl = _get_json(
        SEER_BASE + "render_region_3_controls.php",
        site=1,
        data_type=data_type,
        graph_type=graph_type,
    )
    sites = ctrl["CheckboxValues"]["site"]["values"]
    if len(sites) < 10:
        raise AssertionError(
            f"data_type={data_type}: only {len(sites)} sites from controls "
            "endpoint — expected dozens; shape likely changed"
        )
    return [str(s) for s in sites]


def _flatten_seer(payload: dict, fmts: dict, slug: str, loop_field, loop_val) -> list:
    info = payload.get("info") or {}
    key_order = info.get("key-order") or []
    data_fields = info.get("data-fields") or []
    out = []
    for combo, series_obj in (payload.get("data") or {}).items():
        if not isinstance(series_obj, dict):
            continue
        series = series_obj.get("data_series")
        if not series:
            continue
        dims = dict(zip(key_order, combo.split("_")))
        base = {"statistic": slug}
        for dim, val in dims.items():
            base[dim] = val
            lm = fmts.get(dim)
            if dim in _LABELLED_DIMS and isinstance(lm, dict) and str(val) in lm:
                base[f"{dim}_label"] = lm[str(val)]
        if loop_field is not None:
            base[loop_field] = str(loop_val)
            lm = fmts.get(loop_field)
            if isinstance(lm, dict) and str(loop_val) in lm:
                base[f"{loop_field}_label"] = lm[str(loop_val)]
        for row in series:
            rec = dict(base)
            for field, value in zip(data_fields, row):
                rec[field] = value
            out.append(rec)
    return out


def fetch_seer_statistic(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    slug = node_id[len("nci-seer-explorer-"):]
    cfg = SEER_STATS[slug]
    fmts = _seer_formats()
    sites = _seer_sites(cfg["data_type"], cfg["graph_type"])

    loop_field, loop_vals = cfg["loop"] if cfg["loop"] else (None, [None])

    records = []
    for site in sites:
        for loop_val in loop_vals:
            params = {
                "site": site,
                "data_type": cfg["data_type"],
                "graph_type": cfg["graph_type"],
                "compareBy": "sex",
                "chk_sex_1": 1,
                "chk_sex_3": 1,
                "chk_sex_2": 1,
                "advopt_precision": 1,
                "advopt_show_ci": "on",
            }
            params.update(cfg["fixed"])
            if loop_field is not None:
                params[loop_field] = loop_val
            payload = _get_json(SEER_BASE + "render_region_5.php", **params)
            records.extend(
                _flatten_seer(payload, fmts, slug, loop_field, loop_val)
            )

    if not records:
        raise AssertionError(f"{asset}: fetched 0 records across {len(sites)} sites")
    save_raw_ndjson(records, asset)


# ============================ DOWNLOAD_SPECS ==============================

DOWNLOAD_SPECS = [
    NodeSpec(id="nci-seer-explorer-seer-incidence", fn=fetch_seer_statistic, kind="download"),
    NodeSpec(id="nci-seer-explorer-us-mortality", fn=fetch_seer_statistic, kind="download"),
    NodeSpec(id="nci-seer-explorer-preliminary-incidence-rates", fn=fetch_seer_statistic, kind="download"),
    NodeSpec(id="nci-seer-explorer-survival", fn=fetch_seer_statistic, kind="download"),
    NodeSpec(id="nci-seer-explorer-prevalence", fn=fetch_seer_statistic, kind="download"),
    NodeSpec(id="nci-seer-explorer-risk-of-diagnosis-dying", fn=fetch_seer_statistic, kind="download"),
]


# ============================ TRANSFORM_SPECS =============================

_RATE_SERIES_SQL = """
    SELECT
        site_label                              AS cancer_site,
        TRY_CAST(site AS INTEGER)               AS site_id,
        sex_label                               AS sex,
        race_label                              AS race_ethnicity,
        age_range_label                         AS age_group,
        TRY_CAST(year AS INTEGER)               AS year,
        TRY_CAST(rate AS DOUBLE)                AS rate_per_100k,
        TRY_CAST(rate_lower_ci AS DOUBLE)       AS rate_lower_ci,
        TRY_CAST(rate_upper_ci AS DOUBLE)       AS rate_upper_ci,
        TRY_CAST(modeled_rate AS DOUBLE)        AS modeled_rate,
        TRY_CAST("count" AS BIGINT)             AS case_count
    FROM "{dep}"
    WHERE TRY_CAST(year AS INTEGER) IS NOT NULL
"""

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="nci-seer-explorer-seer-incidence-transform",
        deps=["nci-seer-explorer-seer-incidence"],
        sql=_RATE_SERIES_SQL.format(dep="nci-seer-explorer-seer-incidence"),
    ),
    SqlNodeSpec(
        id="nci-seer-explorer-us-mortality-transform",
        deps=["nci-seer-explorer-us-mortality"],
        sql=_RATE_SERIES_SQL.format(dep="nci-seer-explorer-us-mortality"),
    ),
    SqlNodeSpec(
        id="nci-seer-explorer-preliminary-incidence-rates-transform",
        deps=["nci-seer-explorer-preliminary-incidence-rates"],
        sql=_RATE_SERIES_SQL.format(dep="nci-seer-explorer-preliminary-incidence-rates"),
    ),
    SqlNodeSpec(
        id="nci-seer-explorer-survival-transform",
        deps=["nci-seer-explorer-survival"],
        sql="""
            SELECT
                site_label                            AS cancer_site,
                TRY_CAST(site AS INTEGER)             AS site_id,
                sex_label                             AS sex,
                race_label                            AS race_ethnicity,
                age_range_label                       AS age_group,
                stage_label                           AS stage,
                relative_survival_interval_label      AS survival_interval,
                TRY_CAST(rate AS DOUBLE)              AS relative_survival_pct,
                TRY_CAST(rate_se AS DOUBLE)          AS standard_error,
                TRY_CAST(rate_lower_ci AS DOUBLE)    AS survival_lower_ci,
                TRY_CAST(rate_upper_ci AS DOUBLE)    AS survival_upper_ci,
                TRY_CAST("count" AS BIGINT)          AS case_count
            FROM "nci-seer-explorer-survival"
            WHERE TRY_CAST(rate AS DOUBLE) IS NOT NULL
        """,
    ),
    SqlNodeSpec(
        id="nci-seer-explorer-prevalence-transform",
        deps=["nci-seer-explorer-prevalence"],
        sql="""
            SELECT
                site_label                            AS cancer_site,
                TRY_CAST(site AS INTEGER)             AS site_id,
                sex_label                             AS sex,
                age_range_label                       AS age_group,
                TRY_CAST("count" AS BIGINT)          AS prevalent_cases,
                TRY_CAST(percent AS DOUBLE)          AS prevalence_percent
            FROM "nci-seer-explorer-prevalence"
            WHERE TRY_CAST("count" AS BIGINT) IS NOT NULL
        """,
    ),
    SqlNodeSpec(
        id="nci-seer-explorer-risk-of-diagnosis-dying-transform",
        deps=["nci-seer-explorer-risk-of-diagnosis-dying"],
        sql="""
            SELECT
                site_label                            AS cancer_site,
                TRY_CAST(site AS INTEGER)             AS site_id,
                stat_type_label                       AS risk_type,
                sex_label                             AS sex,
                race_label                            AS race_ethnicity,
                TRY_CAST(risk_interval AS INTEGER)   AS interval_years,
                TRY_CAST(risk AS DOUBLE)             AS risk_percent,
                TRY_CAST(risk_lower_ci AS DOUBLE)    AS risk_lower_ci,
                TRY_CAST(risk_upper_ci AS DOUBLE)    AS risk_upper_ci
            FROM "nci-seer-explorer-risk-of-diagnosis-dying"
            WHERE TRY_CAST(risk AS DOUBLE) IS NOT NULL
        """,
    ),
]
