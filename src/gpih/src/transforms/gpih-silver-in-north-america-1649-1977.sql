-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS "sheet",
    "Year" AS "year",
    "Massachusetts" AS "massachusetts",
    "New York" AS "new_york",
    "New Jersey" AS "new_jersey",
    "Pennsylvania" AS "pennsylvania",
    "Maryland: Hard" AS "maryland_hard",
    "Maryland: Paper" AS "maryland_paper",
    "Virginia" AS "virginia",
    "North Carolina" AS "north_carolina",
    "South Carolina" AS "south_carolina",
    "Georgia" AS "georgia",
    "c11",
    "per troy ounce" AS "per_troy_ounce",
    "per troy ounce_2" AS "per_troy_ounce_2",
    "per gram Ag" AS "per_gram_ag",
    "per gram Ag_2" AS "per_gram_ag_2",
    "£ mint price" AS "mint_price",
    "£ market price" AS "market_price",
    "[P. 319]" AS "p_319",
    "For the period 1720-1774, ""Pennsylvania currency was worth, " AS "for_the_period_1720_1774_pennsylvania_currency_was_worth",
    "c2",
    "c3",
    "c4",
    "c5",
    "c6",
    "c7",
    "c8",
    "Per what" AS "per_what",
    "0.3583" AS "0_3583",
    "31.103" AS "31_103",
    "per dollar" AS "per_dollar",
    "per £" AS "per"
FROM "gpih-silver-in-north-america-1649-1977"
