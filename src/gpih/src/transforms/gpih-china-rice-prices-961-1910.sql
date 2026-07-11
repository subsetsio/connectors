-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS "sheet",
    "1585",
    "0.32" AS "0_32",
    "0.25" AS "0_25",
    "0.33" AS "0_33",
    "0.11004659832246039" AS "0_11004659832246039",
    "0.08597390493942218" AS "0_08597390493942218",
    "0.11348555452003728" AS "0_11348555452003728",
    "Years" AS "years",
    "In Local currency and physical units" AS "in_local_currency_and_physical_units",
    "c2",
    "In grams of silver and metric units" AS "in_grams_of_silver_and_metric_units"
FROM "gpih-china-rice-prices-961-1910"
