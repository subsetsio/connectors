-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "qualified_driving_licence_holders"
FROM "sg-data-d-c043f1858d5fc5a1930cdda165590a33"
