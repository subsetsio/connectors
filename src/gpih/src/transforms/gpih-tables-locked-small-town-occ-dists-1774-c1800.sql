-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS "sheet",
    "Artisan" AS "artisan",
    "0.183" AS "0_183",
    "0.425" AS "0_425",
    "0.294" AS "0_294",
    "0.301" AS "0_301",
    "0.129" AS "0_129",
    "c6",
    "0.6369578637591977" AS "0_6369578637591977",
    "0.15851692638366469" AS "0_15851692638366469",
    "Occupational grouping" AS "occupational_grouping",
    "c1",
    "Number" AS "number",
    "residents",
    "households",
    "Number_2" AS "number_2",
    "residents_2",
    "households_2"
FROM "gpih-tables-locked-small-town-occ-dists-1774-c1800"
