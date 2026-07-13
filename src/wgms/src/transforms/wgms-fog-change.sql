-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "country",
    "glacier_name",
    CAST("glacier_id" AS BIGINT) AS glacier_id,
    "begin_outline_id",
    "end_outline_id",
    CAST("id" AS BIGINT) AS id,
    strptime("begin_date", '%Y-%m-%d')::DATE AS begin_date,
    CAST("begin_date_unc" AS DOUBLE) AS begin_date_unc,
    strptime("end_date", '%Y-%m-%d')::DATE AS end_date,
    CAST("end_date_unc" AS DOUBLE) AS end_date_unc,
    CAST("area" AS BIGINT) AS area,
    CAST("elevation_change" AS DOUBLE) AS elevation_change,
    CAST("elevation_change_unc" AS DOUBLE) AS elevation_change_unc,
    CAST("volume_change" AS BIGINT) AS volume_change,
    CAST("volume_change_unc" AS BIGINT) AS volume_change_unc,
    "begin_platform",
    "begin_method",
    "end_platform",
    "end_method",
    "investigators",
    "agencies",
    "references",
    "remarks"
FROM "wgms-fog-change"
