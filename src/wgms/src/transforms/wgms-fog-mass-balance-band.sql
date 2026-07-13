-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are elevation bands within a glacier-year; glacier-wide balance should come from the glacier-wide table or a weighted aggregation, not a simple row average.
SELECT
    "country",
    "glacier_name",
    CAST("glacier_id" AS BIGINT) AS glacier_id,
    CAST("year" AS BIGINT) AS year,
    CAST("lower_elevation" AS BIGINT) AS lower_elevation,
    CAST("upper_elevation" AS BIGINT) AS upper_elevation,
    CAST("area" AS BIGINT) AS area,
    CAST("winter_balance" AS DOUBLE) AS winter_balance,
    CAST("winter_balance_unc" AS DOUBLE) AS winter_balance_unc,
    CAST("summer_balance" AS DOUBLE) AS summer_balance,
    CAST("summer_balance_unc" AS DOUBLE) AS summer_balance_unc,
    CAST("annual_balance" AS DOUBLE) AS annual_balance,
    CAST("annual_balance_unc" AS DOUBLE) AS annual_balance_unc,
    "remarks"
FROM "wgms-fog-mass-balance-band"
