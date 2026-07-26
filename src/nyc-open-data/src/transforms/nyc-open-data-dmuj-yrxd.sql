-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "city_council_district",
    "of_students_in_grades_68",
    "of_students_in_grades_68_who_have_met_the_requirement_of_54_hours_of_health_instruction",
    "_" AS column,
    "of_8th_graders",
    "of_8th_graders_who_have_met_the_requirement_of_54_hours_of_health_instruction",
    "_1" AS 1
FROM "nyc-open-data-dmuj-yrxd"
