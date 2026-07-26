-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "report_date",
    "building_id",
    "dob_violations",
    "hpd_violations",
    "fdny_violations",
    "total_open_violations"
FROM "nyc-open-data-96te-xmyw"
