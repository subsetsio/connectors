-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Season" AS season,
    "Date" AS date,
    "Date Type" AS date_type,
    "Age Category" AS age_category,
    "Race" AS race,
    "Sex" AS sex,
    "State" AS state,
    "Data Type" AS data_type,
    "Estimate Type" AS estimate_type,
    "Rate Type" AS rate_type,
    CAST("Estimate" AS DOUBLE) AS estimate
FROM "cdc-29hc-w46k"
