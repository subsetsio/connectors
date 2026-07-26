-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "licensing_office",
    "_month" AS month,
    "customers_served",
    "average_wait_time",
    "average_transaction_time",
    "average_satisfaction_rating"
FROM "nyc-open-data-azp6-hepu"
