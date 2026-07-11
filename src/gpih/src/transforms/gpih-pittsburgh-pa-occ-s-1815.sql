-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
SELECT
    "__sheet__" AS sheet,
    "Case_ID" AS case_id,
    "NAMELST" AS namelst,
    "NAMEFST" AS namefst,
    "SEX" AS sex,
    "OCCUP" AS occup,
    "SIDE" AS side,
    "STREET" AS street,
    "BTW" AS btw,
    "CORNER" AS corner,
    "NOTE" AS note
FROM "gpih-pittsburgh-pa-occ-s-1815"
