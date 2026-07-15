-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "race",
    "year",
    "percentage_prog_postsec"
FROM "sg-data-d-c4163aedc16f317ee21cce9c5ea5561d"
