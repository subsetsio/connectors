-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS sheet,
    "Labor" AS labor,
    "396",
    "Revised to 344.30" AS revised_to_344_30,
    "c0",
    "Cash and Board" AS cash_and_board,
    "daily",
    "weekly",
    "monthly",
    "annual",
    "Ratio to Monthly Wage" AS ratio_to_monthly_wage,
    "Annual_1" AS annual_1,
    "c8",
    "c1",
    "c2",
    "Annual*" AS annual_2,
    "Source" AS source,
    "Cash + Board" AS cash_board,
    "Place" AS place,
    "Date" AS date,
    "Food" AS food,
    "Rent" AS rent,
    "Food + Rent" AS food_rent,
    "Payment ($/yr)" AS payment_yr,
    "Notes" AS notes,
    "JGW, June 2011" AS jgw_june_2011,
    "FTE Days per Year for Employed Labor in 1800" AS fte_days_per_year_for_employed_labor_in_1800,
    "e"
FROM "gpih-tables-locked-wage-data-1800"
