-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "from",
    "stamp_duty_type",
    "document_type",
    "holding_period",
    "duty_levied_on",
    "duty_amount",
    "duty_rate"
FROM "sg-data-d-550f42aebb3392f5342a0493a2efdca3"
