-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "Table_Number" AS table_number,
    "Table_name" AS table_name,
    "Table_sub_name" AS table_sub_name,
    "Breakdown" AS breakdown,
    "Section" AS section,
    "Units" AS units,
    "Value" AS value,
    "Time_Period" AS time_period
FROM "statsnz-tatauranga-umanga-maori-statistics-on-maori-businesses-2024-english"
