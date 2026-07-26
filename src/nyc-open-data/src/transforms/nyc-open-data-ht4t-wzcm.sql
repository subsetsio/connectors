-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "license_number",
    "agent_number",
    "hackup_payment_amount",
    "operational_payment_amount",
    "total_payment_amount",
    "payment_date",
    "last_date_updated",
    "last_time_updated"
FROM "nyc-open-data-ht4t-wzcm"
