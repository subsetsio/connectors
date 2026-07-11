-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS sheet,
    "Decade" AS decade,
    "Argentina" AS argentina,
    "Uruguay" AS uruguay,
    "Venezuela" AS venezuela,
    "Mexico" AS mexico,
    "Argentina_2" AS argentina_2,
    "Uruguay_2" AS uruguay_2,
    "Venezuela_2" AS venezuela_2,
    "Mexico_2" AS mexico_2,
    "Argentina_3" AS argentina_3,
    "Uruguay_3" AS uruguay_3,
    "Venezuela_3" AS venezuela_3,
    "Mexico_3" AS mexico_3
FROM "gpih-rent-wage-ratios-latin-america"
