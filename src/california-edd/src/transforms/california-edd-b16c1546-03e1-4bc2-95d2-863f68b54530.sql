-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Age-group unemployment rates are published as separate age columns for the same monthly California observation; do not sum age-rate columns.
SELECT
    CAST("_id" AS BIGINT) AS id,
    "Area Type" AS area_type,
    "Area Name" AS area_name,
    "Date" AS date,
    CAST("Year" AS BIGINT) AS year,
    "Month" AS month,
    CAST("Age 16-19" AS DOUBLE) AS age_16_19,
    CAST("Age 20-24" AS DOUBLE) AS age_20_24,
    CAST("Age 25-34" AS DOUBLE) AS age_25_34,
    CAST("Age 35-44" AS DOUBLE) AS age_35_44,
    CAST("Age 45-54" AS DOUBLE) AS age_45_54,
    CAST("Age 55-64" AS DOUBLE) AS age_55_64,
    CAST("Age 65+" AS DOUBLE) AS age_65
FROM "california-edd-b16c1546-03e1-4bc2-95d2-863f68b54530"
