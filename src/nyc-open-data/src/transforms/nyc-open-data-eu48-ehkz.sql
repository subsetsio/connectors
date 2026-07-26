-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "school_name",
    "grade_level",
    "category",
    "average_frequency_per_week_of_physical_education_instruction",
    "average_minutes_per_week_of_physical_education_instruction",
    "of_students_who_are_receiving_the_required_amount_of_physical_education_instruction",
    "students_receiving_required_amount",
    "of_students_who_are_receiving_less_than_the_required_amount_of_physical_education_instruction",
    "students_receiving_less_than_required_amount",
    "of_students_who_have_an_iep_that_recommends_adaptive_physical_education",
    "students_who_have_an_iep_that_recommends_adaptive_physical_ed"
FROM "nyc-open-data-eu48-ehkz"
