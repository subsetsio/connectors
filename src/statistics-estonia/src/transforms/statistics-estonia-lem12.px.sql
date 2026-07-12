-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "economic_situation_in_comparison_with_five_years_ago",
    "labour_market_situation",
    CAST("year" AS BIGINT) AS year,
    "value"
FROM "statistics-estonia-lem12.px"
