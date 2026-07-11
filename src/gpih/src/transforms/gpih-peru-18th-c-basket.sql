-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
SELECT
    "__sheet__" AS "sheet",
    "Item" AS "item",
    "Hispanic family" AS "hispanic_family",
    "Mestizo family" AS "mestizo_family",
    "1680",
    "1720",
    "1740",
    "1760",
    "1780",
    "1800",
    "1820",
    "1680_2",
    "1720_2",
    "1740_2",
    "1760_2",
    "1780_2",
    "1800_2",
    "1820_2"
FROM "gpih-peru-18th-c-basket"
