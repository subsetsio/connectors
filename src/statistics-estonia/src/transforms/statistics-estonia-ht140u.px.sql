-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "language_of_instruction",
    "form_of_study",
    CAST("reference_period" AS BIGINT) AS reference_period,
    "county_of_residence",
    "education_level",
    "mother_tongue",
    "sex",
    "indicator",
    "value"
FROM "statistics-estonia-ht140u.px"
