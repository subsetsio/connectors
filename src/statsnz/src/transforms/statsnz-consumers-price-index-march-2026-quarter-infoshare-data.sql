-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "Series_Reference" AS series_reference,
    "Period" AS period,
    "Data_Value" AS data_value,
    "Status Code" AS status_code,
    "Type" AS type,
    "Group" AS group,
    "Description" AS description
FROM "statsnz-consumers-price-index-march-2026-quarter-infoshare-data"
