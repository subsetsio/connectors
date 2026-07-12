-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "working_males",
    "working_females",
    "non_working_males",
    "non_working_females"
FROM "qatar-planning-and-statistics-authority-working-and-non-working-members-in-youth-sport-institutions-by-gender"
