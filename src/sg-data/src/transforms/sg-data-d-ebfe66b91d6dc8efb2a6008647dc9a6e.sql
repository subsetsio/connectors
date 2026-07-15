-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "class_of_licence",
    "qualified_driving_licence_holders"
FROM "sg-data-d-ebfe66b91d6dc8efb2a6008647dc9a6e"
