-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "industry",
    "occupation",
    "job_vacancy_rate"
FROM "sg-data-d-ddcb2546c798f94ba6b4a6508ab42632"
