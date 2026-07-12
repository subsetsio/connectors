-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("period" AS DOUBLE) AS period,
    "Series_reference" AS series_reference,
    "Data_value" AS data_value,
    "Units" AS units,
    "STATUS" AS status,
    "Subject" AS subject,
    "Series_title_1" AS series_title_1,
    "Series_title_2" AS series_title_2,
    "Series_title_3" AS series_title_3,
    "Series_title_4" AS series_title_4,
    "Series_title_5" AS series_title_5,
    CAST("Magnitude" AS BIGINT) AS magnitude
FROM "statsnz-na-isal-year-ended-march-2025-sector-accounts"
