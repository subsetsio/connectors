-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "country",
    "glacier_name",
    CAST("glacier_id" AS BIGINT) AS glacier_id,
    CAST("series_id" AS BIGINT) AS series_id,
    strptime("begin_date", '%Y-%m-%d')::DATE AS begin_date,
    CAST("begin_date_unc" AS DOUBLE) AS begin_date_unc,
    strptime("end_date", '%Y-%m-%d')::DATE AS end_date,
    CAST("end_date_unc" AS DOUBLE) AS end_date_unc,
    CAST("length_change" AS BIGINT) AS length_change,
    CAST("length_change_unc" AS DOUBLE) AS length_change_unc,
    "length_change_direction",
    "end_platform",
    "end_method",
    "investigators",
    "agencies",
    "references",
    "remarks"
FROM "wgms-fog-front-variation"
