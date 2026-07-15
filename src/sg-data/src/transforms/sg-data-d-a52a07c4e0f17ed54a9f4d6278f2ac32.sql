-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "no._certified" AS no_certified
FROM "sg-data-d-a52a07c4e0f17ed54a9f4d6278f2ac32"
