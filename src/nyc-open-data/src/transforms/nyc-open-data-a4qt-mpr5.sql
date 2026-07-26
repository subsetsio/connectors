-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough",
    "closuretype",
    "editdate",
    "gispropnum",
    "omppropid",
    "red_sign_installed",
    "status",
    "accessibility",
    "accessibilitylevel",
    "_location" AS location,
    "_name" AS name,
    "rules",
    "_system" AS system,
    "approx_date_closed",
    "approx_date_reopened",
    "community_board",
    "district",
    "latitude",
    "longitude",
    "point"
FROM "nyc-open-data-a4qt-mpr5"
