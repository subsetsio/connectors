-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "country",
    "glacier_name",
    CAST("glacier_id" AS BIGINT) AS glacier_id,
    CAST("outline_id" AS BIGINT) AS outline_id,
    CAST("year" AS BIGINT) AS year,
    "time_system",
    strptime("begin_date", '%Y-%m-%d')::DATE AS begin_date,
    CAST("begin_date_unc" AS DOUBLE) AS begin_date_unc,
    strptime("midseason_date", '%Y-%m-%d')::DATE AS midseason_date,
    CAST("midseason_date_unc" AS DOUBLE) AS midseason_date_unc,
    strptime("end_date", '%Y-%m-%d')::DATE AS end_date,
    CAST("end_date_unc" AS DOUBLE) AS end_date_unc,
    CAST("winter_balance" AS DOUBLE) AS winter_balance,
    CAST("winter_balance_unc" AS DOUBLE) AS winter_balance_unc,
    CAST("summer_balance" AS DOUBLE) AS summer_balance,
    CAST("summer_balance_unc" AS DOUBLE) AS summer_balance_unc,
    CAST("annual_balance" AS DOUBLE) AS annual_balance,
    CAST("annual_balance_unc" AS DOUBLE) AS annual_balance_unc,
    "ela_position",
    CAST("ela" AS BIGINT) AS ela,
    CAST("ela_unc" AS BIGINT) AS ela_unc,
    CAST("aar" AS DOUBLE) AS aar,
    CAST("area" AS BIGINT) AS area,
    "investigators",
    "agencies",
    "references",
    "remarks"
FROM "wgms-fog-mass-balance"
