-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "pct",
    "sector",
    "rank",
    "first_name",
    "last_name",
    "email_address"
FROM "nyc-open-data-rycv-p85i"
