-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("reference_period" AS BIGINT) AS reference_period,
    "generation",
    "knowledge_of_estonian",
    "citizenship",
    "indicator",
    "value"
FROM "statistics-estonia-ir45.px"
