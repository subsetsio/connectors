-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "Series_reference" AS series_reference,
    CAST("Period" AS DOUBLE) AS period,
    CAST("Data_value" AS BIGINT) AS data_value,
    "Suppressed" AS suppressed,
    "STATUS" AS status,
    "UNITS" AS units,
    CAST("Magnitude" AS BIGINT) AS magnitude,
    "Subject" AS subject,
    "Group" AS group,
    "Series_title_1" AS series_title_1,
    "Series_title_2" AS series_title_2,
    "Series_title_3" AS series_title_3,
    "Series_title_4" AS series_title_4,
    "Series_title_5" AS series_title_5
FROM "statsnz-enterprise-counts-march-2023"
