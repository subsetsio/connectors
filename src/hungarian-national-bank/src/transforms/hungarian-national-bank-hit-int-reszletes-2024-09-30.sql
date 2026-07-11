-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Raw rows are workbook cells with worksheet coordinates and metadata; reconstruct the source table layout before interpreting or aggregating values as statistical observations.
SELECT
    "entity_id",
    "source_file_url",
    "source_file_format",
    "source_title",
    "topic",
    "group_name",
    CAST("last_update_date" AS TIMESTAMP) AS last_update_date,
    "next_update_date",
    "sheet_name",
    "row_number",
    "column_number",
    "cell_value",
    "cell_type"
FROM "hungarian-national-bank-hit-int-reszletes-2024-09-30"
