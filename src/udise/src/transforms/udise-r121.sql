-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_udise_report_code" AS udise_report_code,
    "_udise_report_id" AS udise_report_id,
    CAST("_udise_year_id" AS BIGINT) AS udise_year_id,
    "gpi_primary",
    "location_name",
    "gpi_higher_secondary",
    "gpi_elementary",
    "gpi_secondary",
    "gpi_upper_primary"
FROM "udise-r121"
