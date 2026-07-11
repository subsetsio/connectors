-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS sheet,
    "year",
    "quantity",
    "£" AS column,
    "s",
    "d",
    "notes",
    "£ / cord" AS cord,
    "Source: Weeden, Economic and Social History of New England 1" AS source_weeden_economic_and_social_history_of_new_england_1
FROM "gpih-firewood-prices-new-england-1660-1757"
