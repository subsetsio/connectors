-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "licence_type",
    "licence_desc"
FROM "sg-data-d-876921464cb577cb979e5bd75cd7d1c4"
