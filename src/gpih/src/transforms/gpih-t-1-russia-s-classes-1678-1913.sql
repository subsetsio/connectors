-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS "sheet",
    "Estate" AS "estate",
    "c1",
    "1678*" AS "1678",
    "1719*" AS "1719",
    "1762*" AS "1762",
    "1795*" AS "1795",
    "1833*" AS "1833",
    "1858",
    "1870",
    "1897",
    "1913**" AS "1913"
FROM "gpih-t-1-russia-s-classes-1678-1913"
