-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are per economy and day; APNIC also publishes other entity groupings, but this connector currently models the per-economy series only.
SELECT
    "economy",
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "seen",
    "preferred",
    "capable",
    "preferred_pc",
    "capable_pc",
    "preferred_pc_30d",
    "capable_pc_30d"
FROM "apnic-ipv6-capability"
