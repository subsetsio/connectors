-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "industry",
    "occupation",
    "job_vacancy"
FROM "sg-data-d-d3f02543c4d0dd197c56637eefc32624"
