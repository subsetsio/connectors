-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "economic_situation_in_comparison_with_one_year_ago",
    "income_quintile_of_household",
    CAST("year" AS BIGINT) AS year,
    "value"
FROM "statistics-estonia-lem11.px"
