-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS sheet,
    "Year" AS year,
    "Quantity cords" AS quantity_cords,
    "£" AS column,
    "s",
    "d",
    "$" AS column_2,
    "£ /cord" AS cord,
    "$/cord" AS cord_2,
    "page",
    "c9",
    "c10",
    "c11",
    "Quantity" AS quantity,
    "li/cord" AS li_cord,
    "c7",
    "c8",
    "1831",
    "cd",
    "1",
    "Woodstock, Conn." AS woodstock_conn,
    "£/cord" AS cord_3,
    "c6",
    "The New England Historical and Genealogical Register: Vol. 2" AS the_new_england_historical_and_genealogical_register_vol_2,
    "1776",
    "FIREWOOD" AS firewood,
    "CORD" AS cord_4,
    "0.35" AS 0_35,
    "6",
    "0.35_2" AS 0_35_2,
    "year_1",
    "good",
    "unit",
    "raw",
    "quantity_1",
    "Source" AS source,
    "Unit_1" AS unit_1,
    "Type" AS type
FROM "gpih-firewood-prices-1691-1835-seven-locations"
