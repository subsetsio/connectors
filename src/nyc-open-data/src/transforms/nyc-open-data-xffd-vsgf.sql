-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "school",
    "month_code",
    "calmonth",
    "gradelevel",
    "gradesort",
    "roster_count",
    "absent",
    "present",
    "released"
FROM "nyc-open-data-xffd-vsgf"
