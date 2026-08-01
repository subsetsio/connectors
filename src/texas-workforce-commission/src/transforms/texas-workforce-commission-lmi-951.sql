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
    "c003" AS workbook_field_003,
    "c004" AS workbook_field_004,
    "c005" AS workbook_field_005,
    "c006" AS workbook_field_006,
    "c007" AS workbook_field_007,
    "c008" AS workbook_field_008,
    "c009" AS workbook_field_009
FROM "texas-workforce-commission-lmi-951"
