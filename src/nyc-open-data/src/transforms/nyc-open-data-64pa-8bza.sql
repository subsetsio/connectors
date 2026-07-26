-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "school",
    "monthcode",
    "calmonth",
    "schoolyear",
    "gradelevel",
    "gradesort",
    "rostercount",
    "present",
    "absent",
    "released"
FROM "nyc-open-data-64pa-8bza"
