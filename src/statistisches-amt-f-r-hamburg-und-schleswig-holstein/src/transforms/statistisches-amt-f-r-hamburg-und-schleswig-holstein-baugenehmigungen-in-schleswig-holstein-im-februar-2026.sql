-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table is a normalized source-spreadsheet cell extract, not an analysis-ready measure table; reconstruct the source layout with sheet_name, row_number, and column_number before aggregating values.
SELECT
    "package_id",
    "package_title",
    "resource_id",
    "resource_name",
    "resource_format",
    "sheet_name",
    "row_number",
    "column_number",
    "value_text"
FROM "statistisches-amt-f-r-hamburg-und-schleswig-holstein-baugenehmigungen-in-schleswig-holstein-im-februar-2026"
