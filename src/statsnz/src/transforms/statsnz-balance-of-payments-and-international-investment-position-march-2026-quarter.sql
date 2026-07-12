-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "Series_reference" AS series_reference,
    CAST("Period" AS DOUBLE) AS period,
    "Data_value" AS data_value,
    "Suppressed" AS suppressed,
    "STATUS" AS status,
    "UNITS" AS units,
    CAST("MAGNTUDE" AS BIGINT) AS magntude,
    "Subject" AS subject,
    "Group" AS group,
    "Series_title_1" AS series_title_1
FROM "statsnz-balance-of-payments-and-international-investment-position-march-2026-quarter"
