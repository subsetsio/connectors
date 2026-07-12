-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_lsn",
    "university_title",
    "nationality",
    "number_of_teaching_staff_dd_d_hyy_ltdrys",
    "ljnsy",
    "lmsm_ljm_y"
FROM "qatar-planning-and-statistics-authority-number-of-teaching-staff-in-public-colleges-and-universities-by-university-title-and-nationality"
