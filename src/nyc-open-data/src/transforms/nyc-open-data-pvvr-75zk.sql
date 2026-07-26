-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough",
    "closuretype",
    "editdate",
    "gispropnum",
    "_name" AS name,
    "omppropid",
    "parkdistrict",
    "propertyname",
    "red_sign_installed",
    "status",
    "subpropertyname",
    "_system" AS system,
    "yellow_sign_removed",
    "polygon",
    "approx_date_closed",
    "approx_date_reopened"
FROM "nyc-open-data-pvvr-75zk"
