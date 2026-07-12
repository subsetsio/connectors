-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "college",
    "qatari_male",
    "qatari_female",
    "qatari_total",
    "non_qatari_male",
    "non_qatari_female",
    "non_qatari_total",
    "grand_total"
FROM "qatar-planning-and-statistics-authority-student-enrollment-by-college-nationality-and-gender-fall-2024"
