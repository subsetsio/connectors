-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
SELECT
    "__sheet__" AS "sheet",
    "Year" AS "year",
    "per troy ounce" AS "per_troy_ounce",
    "per troy ounce_2" AS "per_troy_ounce_2",
    "per troy ounce_3" AS "per_troy_ounce_3",
    "per troy ounce_4" AS "per_troy_ounce_4",
    "per gram Ag" AS "per_gram_ag",
    "per gram Ag_2" AS "per_gram_ag_2",
    "c7",
    "mint price" AS "mint_price",
    "market price" AS "market_price"
FROM "gpih-silver-value-of-1273-1977"
