-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are elevation bands within a glacier state snapshot; summarize within each state_id before comparing glaciers or dates.
SELECT
    "country",
    "glacier_name",
    CAST("glacier_id" AS BIGINT) AS glacier_id,
    CAST("state_id" AS BIGINT) AS state_id,
    CAST("lower_elevation" AS BIGINT) AS lower_elevation,
    CAST("upper_elevation" AS BIGINT) AS upper_elevation,
    CAST("mean_elevation" AS BIGINT) AS mean_elevation,
    CAST("elevation_unc" AS BIGINT) AS elevation_unc,
    CAST("area" AS BIGINT) AS area,
    CAST("area_unc" AS BIGINT) AS area_unc,
    "remarks"
FROM "wgms-fog-state-band"
