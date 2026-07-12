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
    "STATUS" AS status,
    "UNITS" AS units,
    "Subject" AS subject,
    "Group" AS group,
    "Series_title_1" AS series_title_1
FROM "statsnz-food-price-index-september-2023-index-numbers"
