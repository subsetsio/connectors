-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_resource",
    "source_file",
    "col_0" AS category_group_1,
    "State or jurisdiction" AS state_or_jurisdiction,
    "Number of schools" AS number_of_schools,
    "Percent of students" AS percent_of_students,
    "col_4" AS category_group_2,
    "Number of schools_2" AS number_of_schools_2,
    "Percent of students_2" AS percent_of_students_2,
    "col_7" AS category_group_3,
    "Number of schools_3" AS number_of_schools_3,
    "Percent of students_3" AS percent_of_students_3,
    "col_10" AS category_group_4,
    "Number of schools_4" AS number_of_schools_4,
    "Percent of students_4" AS percent_of_students_4,
    "col_13" AS category_group_5,
    "Number of schools_5" AS number_of_schools_5,
    "Percent of students_5" AS percent_of_students_5,
    "col_16" AS category_group_6,
    "Number of schools_6" AS number_of_schools_6,
    "Percent of students_6" AS percent_of_students_6,
    "col_19" AS category_group_7,
    "col_20" AS category_group_8
FROM "instituto-de-estad-sticas-de-puerto-rico-conjunto-de-datos-comunes-sobre-las-escuelas-publicas"
