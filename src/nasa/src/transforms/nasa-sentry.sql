-- CNEOS Sentry impact-risk list snapshot: one row per monitored object.
-- Envelope values arrive as strings; v_inf carries null-like empties (TRY_CAST).
SELECT
    "des" AS des,
    "id" AS object_id,
    "fullname" AS fullname,
    CAST("h" AS DOUBLE) AS h_mag,
    CAST("diameter" AS DOUBLE) AS diameter_km,
    TRY_CAST("v_inf" AS DOUBLE) AS v_inf_kms,
    CAST("ip" AS DOUBLE) AS impact_prob_cum,
    "n_imp" AS n_impacts,
    CAST("ps_cum" AS DOUBLE) AS palermo_scale_cum,
    CAST("ps_max" AS DOUBLE) AS palermo_scale_max,
    CAST("ts_max" AS BIGINT) AS torino_scale_max,
    "range" AS impact_year_range,
    CAST("last_obs" AS DATE) AS last_obs,
    CAST("last_obs_jd" AS DOUBLE) AS last_obs_jd
FROM "nasa-sentry"
