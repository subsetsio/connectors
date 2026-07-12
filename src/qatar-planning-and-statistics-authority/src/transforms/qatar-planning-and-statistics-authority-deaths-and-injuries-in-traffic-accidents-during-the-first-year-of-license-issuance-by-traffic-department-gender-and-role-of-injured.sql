-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "traffic_department_ar",
    "traffic_department",
    "statement_ar",
    "statement",
    "injured_ar",
    "injured",
    "gender_ar",
    "gender",
    "no_of_people"
FROM "qatar-planning-and-statistics-authority-deaths-and-injuries-in-traffic-accidents-during-the-first-year-of-license-issuance-by-traffic-department-gender-and-role-of-injured"
