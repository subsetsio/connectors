-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "trust_name",
    "first_name",
    "last_name",
    "city",
    "state",
    "zip",
    "donation_date",
    "donation_amount",
    "refund_date",
    "refund_amount",
    "donation_number"
FROM "nyc-open-data-t3pj-3dgu"
