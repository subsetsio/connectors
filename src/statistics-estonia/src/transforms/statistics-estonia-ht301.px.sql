-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "education_level",
    CAST("reference_period" AS BIGINT) AS reference_period,
    "field_of_education",
    "mother_tongue",
    "sex",
    "indicator",
    "value"
FROM "statistics-estonia-ht301.px"
