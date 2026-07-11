-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
SELECT
    "__sheet__" AS sheet,
    "year",
    "unskilled average wage rate (w)" AS unskilled_average_wage_rate_w,
    "unskilled wage rate - 25th percentile (w_25)" AS unskilled_wage_rate_25th_percentile_w_25
FROM "gpih-wages-dahomey-1913-1936-marlous-van-waijenburg"
