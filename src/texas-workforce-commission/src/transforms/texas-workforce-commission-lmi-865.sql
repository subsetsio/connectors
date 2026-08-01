-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "sheet_name",
    "row_number",
    "c001" AS workbook_field_001,
    "c002" AS workbook_field_002,
    "c003" AS workbook_field_003
FROM "texas-workforce-commission-lmi-865"
