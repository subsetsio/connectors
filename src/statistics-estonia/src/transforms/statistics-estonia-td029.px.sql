-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("reference_period" AS BIGINT) AS reference_period,
    "source_of_funds",
    "persons_employed",
    "institutional_sector",
    "indicator",
    "value"
FROM "statistics-estonia-td029.px"
