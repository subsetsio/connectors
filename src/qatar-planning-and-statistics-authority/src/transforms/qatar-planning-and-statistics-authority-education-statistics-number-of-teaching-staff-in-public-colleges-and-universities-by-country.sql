-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_lsn",
    "country",
    "university_title",
    "gender",
    "number_of_teaching_staff_dd_d_hyy_ltdrys",
    "lnw",
    "lmsm_ljm_y",
    "ldwl"
FROM "qatar-planning-and-statistics-authority-education-statistics-number-of-teaching-staff-in-public-colleges-and-universities-by-country"
