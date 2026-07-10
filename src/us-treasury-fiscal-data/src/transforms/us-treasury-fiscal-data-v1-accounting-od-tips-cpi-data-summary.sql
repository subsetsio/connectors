-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "cusip",
    CAST(NULLIF("interest_rate", 'null') AS DOUBLE) AS interest_rate,
    "security_term",
    "original_auction_date",
    "maturity_date",
    "series",
    "original_issue_date",
    "dated_date",
    CAST(NULLIF("ref_cpi_on_dated_date", 'null') AS DOUBLE) AS ref_cpi_on_dated_date,
    "additional_issue_date"
FROM "us-treasury-fiscal-data-v1-accounting-od-tips-cpi-data-summary"
