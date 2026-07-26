-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "fiscal_year",
    "date_range",
    "prompt_payment_interest_rates",
    "net_interest_paid_by_mayoral_agencies_citywide"
FROM "nyc-open-data-qt4e-9a97"
