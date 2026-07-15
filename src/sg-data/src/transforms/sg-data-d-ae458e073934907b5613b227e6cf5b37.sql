-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "name",
    "type",
    "created_at",
    "updated_at",
    "category"
FROM "sg-data-d-ae458e073934907b5613b227e6cf5b37"
