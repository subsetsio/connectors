-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "type_of_citizens",
    "number_of_citizens_held"
FROM "sg-data-d-32e3f5d1425b41da395759c6dc1928df"
