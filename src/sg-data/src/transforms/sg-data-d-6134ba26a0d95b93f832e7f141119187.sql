-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "broadband_connections",
    "no_of_subscriptions"
FROM "sg-data-d-6134ba26a0d95b93f832e7f141119187"
