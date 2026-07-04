-- JPL CNEOS close-approach data: one row per asteroid/comet close approach to
-- Earth, 1900..2100 window. Envelope values arrive as strings; cast to real
-- numerics and parse the non-ISO calendar date ("2026-Jan-01 12:00").
SELECT
    "des" AS des,
    "orbit_id" AS orbit_id,
    CAST("jd" AS DOUBLE) AS jd_tdb,
    strptime("cd", '%Y-%b-%d %H:%M') AS close_approach_time,
    CAST("dist" AS DOUBLE) AS dist_au,
    CAST("dist_min" AS DOUBLE) AS dist_min_au,
    CAST("dist_max" AS DOUBLE) AS dist_max_au,
    CAST("v_rel" AS DOUBLE) AS v_rel_kms,
    CAST("v_inf" AS DOUBLE) AS v_inf_kms,
    "t_sigma_f" AS t_sigma_f,
    CAST("h" AS DOUBLE) AS h_mag
FROM "nasa-cad"
