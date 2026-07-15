-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "period",
    "region",
    "cor",
    "hotel",
    "friends_relatives",
    "others"
FROM "sg-data-d-2b7376e822d2bdc2974f5cdf1709bc24"
