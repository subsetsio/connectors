-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "previous_marital_status",
    "sex",
    CAST("year" AS BIGINT) AS year,
    "value"
FROM "geostat-demography-marriages-35-marriages-by-previous-marital-status-and-sex"
