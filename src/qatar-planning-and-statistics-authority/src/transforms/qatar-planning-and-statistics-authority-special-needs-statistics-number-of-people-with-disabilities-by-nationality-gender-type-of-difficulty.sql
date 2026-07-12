-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "nationality",
    "gender",
    "type_of_difficulty",
    "degree_of_difficulty",
    "number_of_people_with_disabilities_dd_l_frd_dhww_l_qt",
    "degree_of_difficulty_ar",
    "type_of_difficulty_ar",
    "gender_ar",
    "nationality_ar"
FROM "qatar-planning-and-statistics-authority-special-needs-statistics-number-of-people-with-disabilities-by-nationality-gender-type-of-difficulty"
