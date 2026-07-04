-- NHATS human-accessible NEA snapshot: one row per compliant object. The
-- nested min_dv / min_dur dicts were flattened at download (min_dv_dv etc).
-- The API's observation-window / radar-opportunity DATE fields (obs_start,
-- obs_end, radar_obs_a, radar_obs_g) flip between populated and all-null
-- across same-day pulls; all-null makes their inferred type unstable, so they
-- are deliberately not published (obs_mag/obs_flag/radar_snr stay).
SELECT
    "des" AS des,
    trim("fullname") AS fullname,
    CAST("orbit_id" AS BIGINT) AS orbit_id,
    CAST("h" AS DOUBLE) AS h_mag,
    CAST("occ" AS BIGINT) AS orbit_condition_code,
    CAST("min_size" AS DOUBLE) AS min_size_m,
    CAST("max_size" AS DOUBLE) AS max_size_m,
    "size" AS size_m,
    "size_sigma" AS size_sigma_m,
    CAST("min_dv_dv" AS DOUBLE) AS min_dv_kms,
    "min_dv_dur" AS min_dv_duration_days,
    CAST("min_dur_dv" AS DOUBLE) AS min_dur_dv_kms,
    "min_dur_dur" AS min_dur_days,
    "n_via_traj" AS n_trajectories,
    NULLIF(trim("obs_flag"), '') AS obs_flag,
    CAST("obs_mag" AS DOUBLE) AS obs_mag,
    CAST("radar_snr_a" AS DOUBLE) AS radar_snr_arecibo,
    CAST("radar_snr_g" AS DOUBLE) AS radar_snr_goldstone
FROM "nasa-nhats"
