-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS "sheet",
    "row",
    "YEAR" AS "year",
    "CITY" AS "city",
    "STATE" AS "state",
    "LST_NAME" AS "lst_name",
    "FRST_NAME" AS "frst_name",
    "SEX" AS "sex",
    "ADDRESS" AS "address",
    "OCCUPATION" AS "occupation"
FROM "gpih-lexington-ky-1806"
