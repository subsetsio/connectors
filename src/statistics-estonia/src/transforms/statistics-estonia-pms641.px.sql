-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "kind_of_livestock",
    CAST("year" AS BIGINT) AS year,
    "type_of_housing_livestock",
    "indicator",
    "value"
FROM "statistics-estonia-pms641.px"
