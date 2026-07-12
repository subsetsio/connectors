-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "Series_reference" AS series_reference,
    CAST("Period" AS DOUBLE) AS period,
    "Reference_period" AS reference_period,
    CAST("Data_value" AS BIGINT) AS data_value,
    "STATUS" AS status,
    "UNITS" AS units,
    CAST("MAGNTUDE" AS BIGINT) AS magntude,
    "Subject" AS subject,
    "Group" AS group,
    "Series_title" AS series_title
FROM "statsnz-local-authority-statistics-march-2026-quarter"
