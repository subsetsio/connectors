-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "sheet_name",
    "row_number",
    "c001" AS workbook_field_001,
    "c003" AS workbook_field_003,
    "c007" AS workbook_field_007,
    "c011" AS workbook_field_011,
    "c002" AS workbook_field_002,
    "c004" AS workbook_field_004,
    "c005" AS workbook_field_005,
    "c006" AS workbook_field_006,
    "c008" AS workbook_field_008,
    "c009" AS workbook_field_009,
    "c010" AS workbook_field_010,
    "c012" AS workbook_field_012,
    "c013" AS workbook_field_013,
    "c014" AS workbook_field_014
FROM "texas-workforce-commission-lmi-848"
