-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date",
    "program_type",
    "vacancies_per_day",
    "beds_per_day",
    "vacant_per_day"
FROM "nyc-open-data-5rw7-99k7"
