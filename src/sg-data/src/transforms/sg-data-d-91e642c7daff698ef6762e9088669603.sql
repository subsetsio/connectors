-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "race",
    "percentage_pass_eng"
FROM "sg-data-d-91e642c7daff698ef6762e9088669603"
