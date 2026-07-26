-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "district",
    "grade_level",
    "category",
    "average_frequency",
    "average_minutes",
    "of_students_who_are_receiving_the_required_amount_of_physical_education_instruction",
    "of_students_who_are_receiving_the_required_amount_of_physical_education_instruction_1",
    "of_students_who_are_receiving_less_than_the_required_amount_of_physical_education_instruction",
    "of_students_who_are_receiving_less_than_the_required_amount_of_physical_education_instruction_1",
    "of_students_who_have_an_iep_that_recommends_adaptive_physical_education",
    "of_students_who_have_an_iep_that_recommends_adaptive_physical_education_1"
FROM "nyc-open-data-2vha-97jm"
