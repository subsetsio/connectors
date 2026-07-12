-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "lshhr",
    "month",
    "lbyn",
    "statement",
    "lmsb",
    "injured",
    "lnw",
    "gender",
    "no_of_people_dd_l_shkhs"
FROM "qatar-planning-and-statistics-authority-judicial-and-security-services-deaths-and-injuries-in-traffic-accidents-by-month-gender-and-role-of"
