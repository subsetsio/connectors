-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "nationality_ar",
    "nationality",
    "lawyers_working_males",
    "lawyers_working_females",
    "lawyers_under_training_males",
    "lawyers_under_training_females"
FROM "qatar-planning-and-statistics-authority-lawyers-by-gender-and-nationality"
