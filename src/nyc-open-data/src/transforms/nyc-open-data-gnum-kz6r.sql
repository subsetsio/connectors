-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "category_type",
    "category_values",
    "of_students_all_grades",
    "students_taking_cs_all_grades",
    "students_taking_cs_citywide_all_grades",
    "within_cs_all_grades",
    "of_students_grades_k5",
    "students_taking_cs_grades_k5",
    "students_taking_cs_citywide_grades_68",
    "within_cs_grades_k5",
    "of_students_grades_68",
    "students_taking_cs_grades_68",
    "students_taking_cs_citywide_grades_68_1",
    "within_cs_grades_68",
    "of_students_grades_68_1",
    "students_taking_cs_grades_68_1",
    "students_taking_cs_citywide_grades_68_2",
    "within_cs_grades_68_1"
FROM "nyc-open-data-gnum-kz6r"
