-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "NAME" AS name,
    "ADDRESS" AS address,
    "POSTALCODE" AS postalcode,
    "DESCRIPTION" AS description
FROM "sg-data-d-291795a678b8cf82f108780a6235ce18"
