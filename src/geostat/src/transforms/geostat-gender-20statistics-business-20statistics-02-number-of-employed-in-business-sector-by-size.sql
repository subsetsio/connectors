-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "gender",
    "category",
    CAST("year" AS BIGINT) AS year,
    "ownership_type",
    "type_of_activity",
    "value"
FROM "geostat-gender-20statistics-business-20statistics-02-number-of-employed-in-business-sector-by-size"
