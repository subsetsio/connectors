-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "gender",
    "category",
    CAST("year" AS BIGINT) AS year,
    "ownership_type",
    "region",
    "value"
FROM "geostat-gender-20statistics-business-20statistics-01-number-of-employed-in-business-sector-and-average-monthly-remuneratio"
