-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "from",
    "stamp_duty_type",
    "document_type",
    "transaction_type",
    "duty_levied_on",
    "duty_amount",
    "duty_rate"
FROM "sg-data-d-611a3ae502e72fd1ce8adb4e54abfc64"
