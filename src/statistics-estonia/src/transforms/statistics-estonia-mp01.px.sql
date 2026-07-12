-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "county",
    "country_of_residence",
    "indicator",
    CAST("reference_period" AS BIGINT) AS reference_period,
    "value"
FROM "statistics-estonia-mp01.px"
