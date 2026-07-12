-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("column_1" AS BIGINT) AS column_1,
    "column_2",
    "Series_reference" AS series_reference,
    CAST("Period" AS DOUBLE) AS period,
    "Data_value" AS data_value,
    "STATUS" AS status,
    "UNITS" AS units,
    CAST("MAGNTUDE" AS BIGINT) AS magntude,
    "Subject" AS subject,
    "Group" AS group,
    "Series_title_1" AS series_title_1,
    "Series_title_2" AS series_title_2,
    "Series_title_3" AS series_title_3,
    "Series_title_4" AS series_title_4,
    "Series_title_5" AS series_title_5
FROM "statsnz-alcohol-available-for-consumption-year-ended-december-2025"
