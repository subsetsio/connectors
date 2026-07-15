-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "race",
    "year",
    "percentage_progress_postsec"
FROM "sg-data-d-69629447c1a0fd21d70b4c45f027b7e2"
