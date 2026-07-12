-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_udise_report_code" AS udise_report_code,
    "_udise_report_id" AS udise_report_id,
    CAST("_udise_year_id" AS BIGINT) AS udise_year_id,
    "code",
    "school_type",
    "cat8",
    "cat9",
    "cat6",
    "cat7",
    "cat4",
    "locn_name",
    "cat5",
    "total",
    "cat2",
    "cat3",
    "cat1",
    "cat10",
    "cat11"
FROM "udise-r92"
