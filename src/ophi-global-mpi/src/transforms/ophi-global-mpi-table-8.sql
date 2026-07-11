-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Raw rows are non-empty workbook cells, not already-normalized statistical observations; use sheet, row, and column coordinates to reconstruct headers, notes, and data regions before aggregation.
SELECT
    "release_year",
    "table_number",
    "workbook_filename",
    "sheet_name",
    "row_index",
    "column_index",
    "value_text",
    "value_number",
    "value_bool",
    "value_type"
FROM "ophi-global-mpi-table-8"
