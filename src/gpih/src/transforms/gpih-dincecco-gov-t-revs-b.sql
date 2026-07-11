-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
SELECT
    "__sheet__" AS sheet,
    "Country" AS country,
    "Year" AS year,
    "into grams of gold" AS into_grams_of_gold,
    "Population" AS population,
    "per capita" AS per_capita,
    "interpolated)" AS interpolated,
    "1990 $s)" AS 1990_s,
    "Country_2" AS country_2,
    "Year_2" AS year_2,
    "into grams of gold_2" AS into_grams_of_gold_2,
    "Population_2" AS population_2,
    "per capita_2" AS per_capita_2,
    "interpolated)_2" AS interpolated_2,
    "1990 $s)_2" AS 1990_s_2,
    "Country_3" AS country_3,
    "Year_3" AS year_3,
    "into grams of gold_3" AS into_grams_of_gold_3,
    "Population_3" AS population_3,
    "per capita_3" AS per_capita_3,
    "interpolated)_3" AS interpolated_3,
    "1990 $s)_3" AS 1990_s_3,
    "Country_4" AS country_4,
    "Year_4" AS year_4,
    "into grams of gold_4" AS into_grams_of_gold_4,
    "Population_4" AS population_4,
    "per capita_4" AS per_capita_4,
    "interpolated)_4" AS interpolated_4,
    "1990 $s)_4" AS 1990_s_4,
    "Country_5" AS country_5,
    "Year_5" AS year_5,
    "into grams of gold_5" AS into_grams_of_gold_5,
    "Population_5" AS population_5,
    "per capita_5" AS per_capita_5,
    "interpolated)_5" AS interpolated_5,
    "1990 $s)_5" AS 1990_s_5
FROM "gpih-dincecco-gov-t-revs-b"
