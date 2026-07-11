-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
SELECT
    "__sheet__" AS "sheet",
    "Year" AS "year",
    "education",
    "tive expend." AS "tive_expend",
    "schools",
    "schools_2",
    "schools_3",
    "schools_4",
    "education_2",
    "schools_5",
    "check"
FROM "gpih-spain-educ-exp-1850-1965"
