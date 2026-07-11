-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS "sheet",
    "New England" AS "new_england",
    "76000",
    "934000",
    "1010000",
    "0.272" AS "0_272",
    "20672",
    "22407",
    "231641",
    "254048",
    "43079",
    "231641_2",
    "274720"
FROM "gpih-tables-locked-lf-1774-1790-regions-and-sectors"
