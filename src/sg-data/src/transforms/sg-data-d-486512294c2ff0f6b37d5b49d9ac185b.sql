-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "network_access_technology",
    "type_of_plan",
    "number_of_subscriptions"
FROM "sg-data-d-486512294c2ff0f6b37d5b49d9ac185b"
