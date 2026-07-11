-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS sheet,
    "year",
    "month",
    "$/cord" AS cord,
    "Type (unit)" AS type_unit,
    "$/(unit)" AS unit,
    "Notes" AS notes,
    "Source" AS source
FROM "gpih-firewood-prices-washington-dc-1853-1973"
