-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "age_groups_ar",
    "age_groups",
    "statement_ar",
    "statement",
    "injured_ar",
    "injured",
    "gender_ar",
    "gender",
    "no_of_people"
FROM "qatar-planning-and-statistics-authority-deaths-and-injuries-in-traffic-accidents-during-the-first-year-of-license-issuance-by-age-group-gender-and-role-of-injured"
