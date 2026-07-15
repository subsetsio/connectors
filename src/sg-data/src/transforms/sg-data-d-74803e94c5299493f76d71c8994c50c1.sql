-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "industry",
    "occupation",
    "job_vacancy_rate"
FROM "sg-data-d-74803e94c5299493f76d71c8994c50c1"
