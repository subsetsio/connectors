-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS sheet,
    "Artisan" AS artisan,
    "0.183" AS 0_183,
    "0.425" AS 0_425,
    "0.294" AS 0_294,
    "0.301" AS 0_301,
    "0.129" AS 0_129,
    "0.6369578637591977" AS 0_6369578637591977,
    "0.15851692638366469" AS 0_15851692638366469,
    "Officials, professionals" AS officials_professionals,
    "84",
    "0.08641975308641975" AS 0_08641975308641975,
    "White collar" AS white_collar,
    "c4",
    "0.052659860290166574" AS 0_052659860290166574
FROM "gpih-1800-town-rural-occ-dist"
