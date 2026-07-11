-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS sheet,
    "Year" AS year,
    "Price" AS price,
    "Per capita" AS per_capita,
    "Per" AS per,
    "Per_2" AS per_2,
    "Per_3" AS per_3,
    "Real" AS real,
    "Per capita_2" AS per_capita_2,
    "Weight" AS weight,
    "Malanima" AS malanima,
    "Malanima_2" AS malanima_2,
    "Log-linearly" AS log_linearly,
    "Nominal GDP" AS nominal_gdp,
    "Nominal GDP_2" AS nominal_gdp_2
FROM "gpih-italy-malanima-cn-gnp-1310-1913"
