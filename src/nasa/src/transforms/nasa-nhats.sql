-- NHATS human-accessible NEA snapshot: one row per compliant object. The
-- nested min_dv / min_dur dicts were flattened at download (min_dv_dv etc).
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
    "obs_start" AS obs_window_start,
    "obs_end" AS obs_window_end,
    NULLIF(trim("obs_flag"), '') AS obs_flag,
    CAST("obs_mag" AS DOUBLE) AS obs_mag,
    "radar_obs_a" AS radar_obs_arecibo,
    "radar_obs_g" AS radar_obs_goldstone,
    CAST("radar_snr_a" AS DOUBLE) AS radar_snr_arecibo,
    CAST("radar_snr_g" AS DOUBLE) AS radar_snr_goldstone
FROM "nasa-nhats"
