-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "country",
    "glacier_name",
    CAST("glacier_id" AS BIGINT) AS glacier_id,
    "outline_id",
    CAST("id" AS BIGINT) AS id,
    strptime("date", '%Y-%m-%d')::DATE AS date,
    CAST("date_unc" AS DOUBLE) AS date_unc,
    CAST("highest_elevation" AS BIGINT) AS highest_elevation,
    CAST("lowest_elevation" AS BIGINT) AS lowest_elevation,
    CAST("mean_elevation" AS BIGINT) AS mean_elevation,
    CAST("elevation_unc" AS BIGINT) AS elevation_unc,
    CAST("area" AS BIGINT) AS area,
    CAST("area_unc" AS BIGINT) AS area_unc,
    CAST("length" AS BIGINT) AS length,
    CAST("length_unc" AS BIGINT) AS length_unc,
    "terminus_type",
    "platform",
    "method",
    "investigators",
    "agencies",
    "references",
    "remarks"
FROM "wgms-fog-state"
