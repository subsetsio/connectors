-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "school",
    "monthcode",
    "calmonth",
    "gradelevel",
    "gradesort",
    "rostercount",
    "absent",
    "present",
    "released",
    "tot"
FROM "nyc-open-data-7u63-ib3x"
