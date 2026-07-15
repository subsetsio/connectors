-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "yr",
    "type_of_grounds",
    "no_of_claims"
FROM "sg-data-d-0d502e1bb055ae4a570797bf913b5c9d"
