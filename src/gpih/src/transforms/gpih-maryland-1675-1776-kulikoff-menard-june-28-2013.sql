-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
SELECT
    "__sheet__" AS sheet,
    "For slave prices," AS for_slave_prices,
    "c1",
    "Centered" AS centered,
    "No. of" AS no_of,
    "Price in MD" AS price_in_md,
    "No. of_2" AS no_of_2,
    "Price in MD_2" AS price_in_md_2,
    "No. of_3" AS no_of_3,
    "Price in MD_3" AS price_in_md_3,
    "No. of_4" AS no_of_4,
    "Price in MD_4" AS price_in_md_4,
    "No. of_5" AS no_of_5,
    "Price in MD_5" AS price_in_md_5,
    "c13",
    "and slaves" AS and_slaves,
    "Commodities" AS commodities,
    "factured goods" AS factured_goods,
    "commodities_1",
    "c18"
FROM "gpih-maryland-1675-1776-kulikoff-menard-june-28-2013"
