-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "job_vacancy_rate"
FROM "sg-data-d-fb4853f65d48be0a6ee7fb762b1b5251"
