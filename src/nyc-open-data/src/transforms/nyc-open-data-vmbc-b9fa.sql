-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough",
    "grade_level",
    "category",
    "category_1",
    "average_frequency",
    "average_minutes",
    "of_students_who_are_receiving_the_required_amount_of_physical_education_instruction",
    "_" AS column,
    "of_students_who_are_receiving_less_than_the_required_amount_of_physical_education_instruction",
    "_1" AS 1,
    "of_students_who_have_an_iep_that_recommends_adaptive_physical_education",
    "_2" AS 2
FROM "nyc-open-data-vmbc-b9fa"
