-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Measure_ID" AS measure_id,
    "Measure_statement_full" AS measure_statement_full,
    "Measures_statement_short" AS measures_statement_short,
    "Category" AS category,
    "Population" AS population,
    CAST("Year" AS BIGINT) AS year,
    CAST("Estimate" AS DOUBLE) AS estimate,
    CAST("SE" AS DOUBLE) AS se,
    "Unit" AS unit,
    "Flag" AS flag
FROM "cdc-f3a8-hmpp"
