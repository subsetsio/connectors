-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("period" AS BIGINT) AS period,
    "nuts",
    "age",
    "sex",
    CAST("icd10" AS BIGINT) AS icd10,
    "unit",
    "value"
FROM "statistics-bulgaria-1678"
