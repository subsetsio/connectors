-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_udise_report_code" AS udise_report_code,
    "_udise_report_id" AS udise_report_id,
    CAST("_udise_year_id" AS BIGINT) AS udise_year_id,
    "sch_mgmt_id",
    "location_name",
    "trained_cwsn_f",
    "trained_cwsn",
    "trained_cwsn_m",
    "sch_mgmt_name"
FROM "udise-r129"
