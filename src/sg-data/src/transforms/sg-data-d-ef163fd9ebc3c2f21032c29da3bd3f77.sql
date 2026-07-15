-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "abbreviation",
    "political_party"
FROM "sg-data-d-ef163fd9ebc3c2f21032c29da3bd3f77"
