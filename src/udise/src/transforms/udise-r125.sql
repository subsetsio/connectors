-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_udise_report_code" AS udise_report_code,
    "_udise_report_id" AS udise_report_id,
    CAST("_udise_year_id" AS BIGINT) AS udise_year_id,
    "rr8_b",
    "rr12_b",
    "rr10_g",
    "rr5_b",
    "rr5_g",
    "rr10_b",
    "rr10",
    "rr12_g",
    "rr5",
    "rr12",
    "state_name",
    "rr8",
    "rr8_g",
    "state_cd"
FROM "udise-r125"
