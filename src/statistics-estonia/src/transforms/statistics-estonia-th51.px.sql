-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("reference_period" AS BIGINT) AS reference_period,
    "access_to_healthcare",
    "kind_of_healthcare",
    "income_group",
    "indicator",
    "value"
FROM "statistics-estonia-th51.px"
