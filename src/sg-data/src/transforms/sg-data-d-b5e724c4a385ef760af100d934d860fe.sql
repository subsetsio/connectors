-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "type_of_fixed_lines",
    "number_of_subscriptions"
FROM "sg-data-d-b5e724c4a385ef760af100d934d860fe"
