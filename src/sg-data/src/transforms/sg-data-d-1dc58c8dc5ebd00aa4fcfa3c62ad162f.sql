-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "illegal_immigrants_count"
FROM "sg-data-d-1dc58c8dc5ebd00aa4fcfa3c62ad162f"
