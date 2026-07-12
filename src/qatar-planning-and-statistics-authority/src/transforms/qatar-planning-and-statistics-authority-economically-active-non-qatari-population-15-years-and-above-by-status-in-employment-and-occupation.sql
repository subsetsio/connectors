-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "occupation",
    "lmhn",
    "employer",
    "own_account_worker",
    "employee",
    "unpaid_family_worker",
    "total",
    "skill_level",
    "skill_level_ar"
FROM "qatar-planning-and-statistics-authority-economically-active-non-qatari-population-15-years-and-above-by-status-in-employment-and-occupation"
