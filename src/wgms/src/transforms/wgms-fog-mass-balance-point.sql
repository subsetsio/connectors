-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "country",
    "glacier_name",
    CAST("glacier_id" AS BIGINT) AS glacier_id,
    CAST("year" AS BIGINT) AS year,
    CAST("id" AS BIGINT) AS id,
    "original_id",
    "time_system",
    strptime("begin_date", '%Y-%m-%d')::DATE AS begin_date,
    CAST("begin_date_unc" AS DOUBLE) AS begin_date_unc,
    strptime("end_date", '%Y-%m-%d')::DATE AS end_date,
    CAST("end_date_unc" AS DOUBLE) AS end_date_unc,
    CAST("latitude" AS DOUBLE) AS latitude,
    CAST("longitude" AS DOUBLE) AS longitude,
    CAST("elevation" AS BIGINT) AS elevation,
    CAST("balance" AS DOUBLE) AS balance,
    CAST("balance_unc" AS DOUBLE) AS balance_unc,
    CAST("density" AS BIGINT) AS density,
    CAST("density_unc" AS BIGINT) AS density_unc,
    "method",
    "balance_code",
    "remarks"
FROM "wgms-fog-mass-balance-point"
