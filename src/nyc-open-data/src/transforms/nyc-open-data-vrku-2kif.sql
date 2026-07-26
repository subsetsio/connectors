-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "school",
    "monthcode",
    "calmonth",
    "schoolyear",
    "grade_level",
    "grade_sort",
    "rostercount",
    "present",
    "absent",
    "_release" AS release
FROM "nyc-open-data-vrku-2kif"
