-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "record_id",
    "date_opened",
    "business_name",
    "business_name_2",
    "industry",
    "withdrawal_from",
    "basis_for_withdrawal",
    "amount",
    "date_completed"
FROM "nyc-open-data-ga3c-v25a"
