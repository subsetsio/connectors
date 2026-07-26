-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough",
    "cemspermittable",
    "closuretype",
    "dimensions",
    "editdate",
    "fieldnumber",
    "gispropnum",
    "_name" AS name,
    "netsrimsgoals_removed",
    "omppropid",
    "parkdistrict",
    "primarysport",
    "propertyname",
    "red_sign_installed",
    "status",
    "subpropertyname",
    "surfacetype",
    "_system" AS system,
    "yellow_sign_removed",
    "polygon",
    "approx_date_closed",
    "approx_date_reopened",
    "approx_date_netsrimsgoals_added",
    "netsrimsgoals_added"
FROM "nyc-open-data-g3xg-qtbc"
