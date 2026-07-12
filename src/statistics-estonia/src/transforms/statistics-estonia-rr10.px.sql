-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "national_accounts",
    "quarter",
    CAST("year" AS BIGINT) AS year,
    "counterpart",
    "sector",
    "indicator",
    "financial_transactions_and_balance_sheet",
    "value"
FROM "statistics-estonia-rr10.px"
