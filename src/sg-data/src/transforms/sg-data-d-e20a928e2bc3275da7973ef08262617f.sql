-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "escape_rate_per_10000_inmates"
FROM "sg-data-d-e20a928e2bc3275da7973ef08262617f"
