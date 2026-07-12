-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_lsn",
    "level_of_education",
    "type_of_school",
    "number_of_classrooms_dd_lsfwf",
    "number_of_schools_dd_lmdrs",
    "number_of_female_teachers_dd_lmdrsyn_lnth",
    "number_of_male_teachers_dd_lmdrsyn_ldhkwr",
    "number_of_students_dd_ltlb",
    "nw_lmdrs",
    "lmrhl_lt_lymy"
FROM "qatar-planning-and-statistics-authority-education-statistics-number-of-public-schools-and-their-classes-students-and-teachers-by-level-of"
