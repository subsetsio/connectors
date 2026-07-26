-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "report_category",
    "school_level",
    "geographic_unit",
    "school_name",
    "student_category",
    "code",
    "discharge_category",
    "discharge_description",
    "count_of_students",
    "total_enrolled_students"
FROM "nyc-open-data-a2gn-nyzs"
