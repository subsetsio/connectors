-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS "sheet",
    "year",
    "month",
    "$/cord" AS "cord",
    "Type" AS "type",
    "Notes" AS "notes",
    "Source: Atlanta Journal-Constitution, Atlanta Daily News" AS "source_atlanta_journal_constitution_atlanta_daily_news"
FROM "gpih-firewood-prices-atlanta-1869-1922"
