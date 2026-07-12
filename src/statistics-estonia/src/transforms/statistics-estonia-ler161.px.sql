-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "kind_of_dwelling",
    "labour_market_situation_of_the_household",
    CAST("year" AS BIGINT) AS year,
    "value"
FROM "statistics-estonia-ler161.px"
