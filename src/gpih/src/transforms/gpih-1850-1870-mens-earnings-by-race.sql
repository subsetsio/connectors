-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    CAST("__sheet__" AS BIGINT) AS sheet,
    "Year" AS year,
    "Region" AS region,
    "Avg Wage" AS avg_wage,
    "Total Perwt Wage" AS total_perwt_wage,
    "Number of men perwt" AS number_of_men_perwt,
    "Avg Wage_2" AS avg_wage_2,
    "Total Perwt Wage_2" AS total_perwt_wage_2,
    "Number of men perwt_2" AS number_of_men_perwt_2,
    "c8",
    "Avg Wage_3" AS avg_wage_3,
    "Total Perwt Wage_3" AS total_perwt_wage_3,
    "Number of men perwt_3" AS number_of_men_perwt_3,
    "Avg Wage_4" AS avg_wage_4,
    "Total Perwt Wage_4" AS total_perwt_wage_4,
    "Number of men perwt_4" AS number_of_men_perwt_4,
    "Avg Wage_5" AS avg_wage_5,
    "Total Perwt Wage_5" AS total_perwt_wage_5,
    "Number of men perwt_5" AS number_of_men_perwt_5,
    "Avg Wage_6" AS avg_wage_6,
    "Total Perwt Wage_6" AS total_perwt_wage_6,
    "Number of men perwt_6" AS number_of_men_perwt_6,
    "Avg Wage_7" AS avg_wage_7,
    "Total Perwt Wage_7" AS total_perwt_wage_7,
    "Number of men perwt_7" AS number_of_men_perwt_7,
    "Avg Wage_8" AS avg_wage_8,
    "Total Perwt Wage_8" AS total_perwt_wage_8,
    "Number of men perwt_8" AS number_of_men_perwt_8,
    "small n's" AS small_n_s,
    "small n's_2" AS small_n_s_2
FROM "gpih-1850-1870-mens-earnings-by-race"
