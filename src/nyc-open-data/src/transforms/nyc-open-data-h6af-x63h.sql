-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "_session" AS session,
    "borough",
    "swimming_pool",
    "class_type",
    "class_time",
    "of_classes",
    "total_registration",
    "week_1_total_attendance",
    "week_2_total_attendance",
    "week_3_total_attendance",
    "total_attendance"
FROM "nyc-open-data-h6af-x63h"
