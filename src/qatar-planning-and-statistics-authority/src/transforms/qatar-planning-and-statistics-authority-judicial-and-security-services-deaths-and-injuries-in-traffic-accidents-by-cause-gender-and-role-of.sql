-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sbb_lhdth",
    "cause",
    "lbyn",
    "statement",
    "lmsb",
    "injured",
    "lnw",
    "gender",
    "dd_l_shkhs_no_of_people"
FROM "qatar-planning-and-statistics-authority-judicial-and-security-services-deaths-and-injuries-in-traffic-accidents-by-cause-gender-and-role-of"
