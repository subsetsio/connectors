-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
SELECT
    "__sheet__" AS sheet,
    "Region" AS region,
    "Average Household Incomea in Baht" AS average_household_incomea_in_baht,
    "Average Household Expendituresb in Baht" AS average_household_expendituresb_in_baht,
    "Average Household Incomea in pound Sterling" AS average_household_incomea_in_pound_sterling,
    "Average Household Expendituresb in pound Sterling" AS average_household_expendituresb_in_pound_sterling,
    "Direct Taxes" AS direct_taxes,
    "Food" AS food,
    "Clothing" AS clothing,
    "Household" AS household,
    "Interest" AS interest,
    "Other" AS other,
    "Rice as a Percent of Total Incomec" AS rice_as_a_percent_of_total_incomec,
    "Average Household Income in Bahtd" AS average_household_income_in_bahtd,
    "Average Household Expenditures in Bahte" AS average_household_expenditures_in_bahte,
    "Average Household Income in pound Sterlingd" AS average_household_income_in_pound_sterlingd,
    "Average Household Expenditures in pound Sterlinge" AS average_household_expenditures_in_pound_sterlinge
FROM "gpih-thai-household-budgets-1930-35"
