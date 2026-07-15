-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "industry",
    "occupation",
    "job_vacancy"
FROM "sg-data-d-889d11a2b0a53b235abb64e3f4e0a47b"
