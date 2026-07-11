-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS "sheet",
    "Year" AS "year",
    "Pound Sterling per metric ton" AS "pound_sterling_per_metric_ton",
    "Nominal Unskilled Bangkok Wage in Baht per Day" AS "nominal_unskilled_bangkok_wage_in_baht_per_day",
    "Rural or Agricultural Wage in Baht" AS "rural_or_agricultural_wage_in_baht",
    "Nominal Unskilled Bangkok Wage in pound Sterling per Day" AS "nominal_unskilled_bangkok_wage_in_pound_sterling_per_day",
    "Rural or Agricultural Wage in pound Sterling per Day" AS "rural_or_agricultural_wage_in_pound_sterling_per_day",
    "Source" AS "source",
    "Import Price of White Shirting in Baht per Kilogram" AS "import_price_of_white_shirting_in_baht_per_kilogram",
    "Import Price of Grey Shirting in Baht per Kilogram" AS "import_price_of_grey_shirting_in_baht_per_kilogram",
    "Import Price of White Shirting in pound Sterling per Kilogra" AS "import_price_of_white_shirting_in_pound_sterling_per_kilogra",
    "Import Price of Grey Shirting in pound Sterling per Kilogram" AS "import_price_of_grey_shirting_in_pound_sterling_per_kilogram",
    "Land Price in Baht per Rai" AS "land_price_in_baht_per_rai",
    "Land Price in pound Sterling per Rai" AS "land_price_in_pound_sterling_per_rai",
    "Location" AS "location",
    "Land Price in Baht per acre" AS "land_price_in_baht_per_acre",
    "Land Price in pound Sterling per acre" AS "land_price_in_pound_sterling_per_acre",
    "Average Baht per Hectare of Newly Mortgaged Land" AS "average_baht_per_hectare_of_newly_mortgaged_land",
    "Average pound Sterling per Hectare of Newly Mortgaged Land" AS "average_pound_sterling_per_hectare_of_newly_mortgaged_land",
    "Nominal Buffalo Export Price in Baht" AS "nominal_buffalo_export_price_in_baht",
    "Nominal Buffalo Export Price in pound Sterling" AS "nominal_buffalo_export_price_in_pound_sterling"
FROM "gpih-thai-prices-and-wages-1820-1959"
