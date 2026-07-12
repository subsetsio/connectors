-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "type_of_security",
    "type_of_security_ar",
    "2019_males",
    "2019_females",
    "2020_males",
    "2020_females",
    "2021_males",
    "2021_females",
    "2022_males",
    "2022_females",
    "2023_males",
    "2023_females"
FROM "qatar-planning-and-statistics-authority-beneficiaries-of-the-social-security-by-type-of-security-and-gender"
