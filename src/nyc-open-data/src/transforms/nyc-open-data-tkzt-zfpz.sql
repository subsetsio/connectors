-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough",
    "closuretype",
    "editdate",
    "featuretype",
    "propid",
    "propname",
    "propnum",
    "sitename",
    "status",
    "point",
    "approx_date_closed",
    "approx_date_reopened"
FROM "nyc-open-data-tkzt-zfpz"
