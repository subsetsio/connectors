-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are elevation bands within a geodetic change record; band values are components of a parent observation, not independent glacier-level observations.
SELECT
    "country",
    "glacier_name",
    CAST("glacier_id" AS BIGINT) AS glacier_id,
    CAST("change_id" AS BIGINT) AS change_id,
    CAST("lower_elevation" AS BIGINT) AS lower_elevation,
    CAST("upper_elevation" AS BIGINT) AS upper_elevation,
    CAST("area" AS BIGINT) AS area,
    CAST("elevation_change" AS DOUBLE) AS elevation_change,
    CAST("elevation_change_unc" AS DOUBLE) AS elevation_change_unc,
    CAST("volume_change" AS BIGINT) AS volume_change,
    CAST("volume_change_unc" AS BIGINT) AS volume_change_unc,
    "remarks"
FROM "wgms-fog-change-band"
