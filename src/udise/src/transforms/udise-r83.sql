-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This report is a wide UDISE+ cross-tab with no verified row key in the raw profile; treat rows as report records and filter the relevant dimensions before aggregating values.
SELECT
    "_udise_report_code" AS udise_report_code,
    "_udise_report_id" AS udise_report_id,
    CAST("_udise_year_id" AS BIGINT) AS udise_year_id,
    "code",
    "cat8",
    "cat9",
    "cat6",
    "cat7",
    "cat4",
    "locn_name",
    "cat5",
    "sch_mgmt_id",
    "total",
    "cat2",
    "cat3",
    "cat1",
    "cat10",
    "cat11",
    "sch_mgmt_name"
FROM "udise-r83"
