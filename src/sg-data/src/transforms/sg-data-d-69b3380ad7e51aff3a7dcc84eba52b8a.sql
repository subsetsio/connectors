-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "bidding_no",
    "vehicle_class",
    "quota",
    "bids_success",
    "bids_received",
    "premium"
FROM "sg-data-d-69b3380ad7e51aff3a7dcc84eba52b8a"
