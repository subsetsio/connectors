-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
SELECT
    "__sheet__" AS sheet,
    "1831-1835" AS 1831_1835,
    "150.93687712019772" AS 150_93687712019772,
    "123.1603937226333" AS 123_1603937226333,
    "0.2626241395141806" AS 0_2626241395141806,
    "33.72801935789611" AS 33_72801935789611
FROM "gpih-arroyo-abad-2013b"
