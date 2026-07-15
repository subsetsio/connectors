-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "specialisation",
    "no_of_schools"
FROM "sg-data-d-1f1faa635f8695c307ec6ca5261a4578"
