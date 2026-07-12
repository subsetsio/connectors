-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "kind_of_livestock",
    CAST("year" AS BIGINT) AS year,
    "amount_of_time_of_grazing",
    "indicator",
    "value"
FROM "statistics-estonia-pms642.px"
