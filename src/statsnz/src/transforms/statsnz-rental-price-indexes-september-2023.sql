-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "SER_REF" AS ser_ref,
    CAST("TIME_REF" AS DOUBLE) AS time_ref,
    CAST("DATA_VAL" AS BIGINT) AS data_val,
    "STATUS" AS status,
    "UNITS" AS units,
    "Subject" AS subject,
    "Group" AS group,
    "Series_title_1" AS series_title_1,
    "Series_title_2" AS series_title_2,
    "Series_title_3" AS series_title_3
FROM "statsnz-rental-price-indexes-september-2023"
