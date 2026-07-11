-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "report_number",
    "freq_type",
    CAST("mask" AS BIGINT) AS mask,
    "indicator",
    CAST("col_label" AS BIGINT) AS col_label,
    CAST("value" AS DOUBLE) AS value
FROM "beijing-municipal-bureau-of-statistics-01-qy-115-2013-1002-1"
