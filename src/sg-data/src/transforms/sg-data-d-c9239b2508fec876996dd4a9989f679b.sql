-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "speed",
    "no_of_subscriptions"
FROM "sg-data-d-c9239b2508fec876996dd4a9989f679b"
