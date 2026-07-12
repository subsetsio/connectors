-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_udise_report_code" AS udise_report_code,
    "_udise_report_id" AS udise_report_id,
    CAST("_udise_year_id" AS BIGINT) AS udise_year_id,
    "field1",
    "total",
    "other",
    "cnt_govt",
    "govt_aid",
    "state_name",
    "cum_total",
    "year_id",
    "state_cd",
    "st_govt",
    "estd_year",
    "pvt"
FROM "udise-r152"
