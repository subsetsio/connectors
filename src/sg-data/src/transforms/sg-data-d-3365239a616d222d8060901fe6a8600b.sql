-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "from",
    "document_type",
    "lease_term",
    "duty_levied_on",
    "duty_amount",
    "duty_rate",
    "maximum_duty"
FROM "sg-data-d-3365239a616d222d8060901fe6a8600b"
