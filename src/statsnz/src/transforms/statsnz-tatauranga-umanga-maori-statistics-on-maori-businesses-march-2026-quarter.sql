-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("Table_Number" AS BIGINT) AS table_number,
    "Table_Name" AS table_name,
    "Table_Sub_Name" AS table_sub_name,
    "Table_Section" AS table_section,
    "Breakdown" AS breakdown,
    CAST("Quarter" AS BIGINT) AS quarter,
    "Unit" AS unit,
    "Value" AS value
FROM "statsnz-tatauranga-umanga-maori-statistics-on-maori-businesses-march-2026-quarter"
