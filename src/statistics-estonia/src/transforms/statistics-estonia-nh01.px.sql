-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "indicator",
    "age_group",
    CAST("year" AS BIGINT) AS year,
    "administrative_unit",
    "sex",
    "value"
FROM "statistics-estonia-nh01.px"
