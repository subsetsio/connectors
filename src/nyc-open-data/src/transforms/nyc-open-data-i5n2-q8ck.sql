-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "approx_date_closed",
    "approx_date_reopened",
    "bin",
    "borough",
    "closuretype",
    "doittid",
    "editdate",
    "gispropnum",
    "omppropid",
    "parkdistrict",
    "status",
    "_system" AS system,
    "polygon"
FROM "nyc-open-data-i5n2-q8ck"
