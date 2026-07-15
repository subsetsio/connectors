-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "POSTALCODE" AS postalcode,
    "NAME" AS name,
    "ADDRESS" AS address
FROM "sg-data-d-9d7aaaaad7cf2646e82689ab87d1c1a1"
