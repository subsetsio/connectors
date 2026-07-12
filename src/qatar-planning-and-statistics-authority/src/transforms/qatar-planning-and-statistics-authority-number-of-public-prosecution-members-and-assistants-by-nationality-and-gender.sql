-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "nationality",
    "gender",
    "number_of_members_and_assistants",
    "gender_ar",
    "nationality_ar"
FROM "qatar-planning-and-statistics-authority-number-of-public-prosecution-members-and-assistants-by-nationality-and-gender"
