-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "january_2019_service_type",
    "grade",
    "school_type",
    "of_students_assigned_to_service",
    "unnamed_column",
    "february_2019_service_type",
    "grade_1",
    "school_type_1",
    "of_students_assigned_to_service_1",
    "unnamed_column_1",
    "march_2019_service_type",
    "grade_2",
    "school_type_2",
    "of_students_assigned_to_service_2",
    "unnamed_column_2",
    "april_2019_service_type",
    "grade_3",
    "school_type_3",
    "of_students_assigned_to_service_3",
    "unnamed_column_3",
    "may_2019_service_type",
    "grade_4",
    "school_type_4",
    "of_students_assigned_to_service_4",
    "unnamed_column_4",
    "june_2019_service_type",
    "grade_5",
    "school_type_5",
    "of_students_assigned_to_service_5"
FROM "nyc-open-data-r2j4-rc64"
