-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "occupation",
    "job_vacancy_rate"
FROM "sg-data-d-1e10046c33418c507bb2483c26dca489"
