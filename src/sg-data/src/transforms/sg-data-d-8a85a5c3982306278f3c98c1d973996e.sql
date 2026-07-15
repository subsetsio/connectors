-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Year" AS year,
    "School" AS school,
    "Course_Type" AS course_type,
    "Course_Name" AS course_name,
    "Gender" AS gender,
    "No_of_Students" AS no_of_students
FROM "sg-data-d-8a85a5c3982306278f3c98c1d973996e"
