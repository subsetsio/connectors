-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "provider_name",
    "program_name",
    CAST("all_students_7_1_2018_6_30" AS BIGINT) AS all_students_7_1_2018_6_30,
    CAST("all_student_exiters_7_1_2018" AS BIGINT) AS all_student_exiters_7_1_2018,
    CAST("all_students_successfully" AS BIGINT) AS all_students_successfully,
    "all_students_percent",
    "percent_received_credential",
    CAST("received_credential" AS BIGINT) AS received_credential
FROM "texas-workforce-commission-socrata-d3pe-3f9f"
