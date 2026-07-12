-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sector",
    "instrument_of_the_national_accounts_esa_2010",
    "indicator",
    CAST("year" AS BIGINT) AS year,
    "value"
FROM "statistics-estonia-rak001.px"
