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
FROM "sg-data-d-9d5be2e6cabd1e7da5f95eaea69ab069"
