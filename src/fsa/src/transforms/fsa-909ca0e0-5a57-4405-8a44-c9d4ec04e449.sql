-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is a normalized spreadsheet-cell table. Use resource_id, sheet, row_idx, and col_idx to reconstruct source rows and columns; do not aggregate num_value without interpreting the surrounding labels in value.
SELECT
    "resource_id",
    "resource_name",
    CAST("sheet" AS BIGINT) AS sheet,
    "row_idx",
    "col_idx",
    "value",
    "num_value"
FROM "fsa-909ca0e0-5a57-4405-8a44-c9d4ec04e449"
