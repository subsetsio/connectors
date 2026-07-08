SELECT
    "Country"                                        AS country,
    TRY_CAST("Date Announced" AS DATE)               AS date_announced,
    "Time Horizon"                                   AS time_horizon,
    "Status"                                         AS status,
    "Measure Name"                                   AS measure_name,
    "Details"                                        AS details,
    "Broad Measure Type"                             AS broad_measure_type,
    "Specific Measure Type"                          AS specific_measure_type,
    "Energy carrier"                                 AS energy_carrier,
    "Target Group"                                   AS target_group,
    TRY_CAST("Total Amount (in billion euros)" AS DOUBLE)  AS total_amount_billion_eur,
    TRY_CAST("GDP (in billion euros)" AS DOUBLE)           AS gdp_billion_eur,
    TRY_CAST("Measure in % of GDP" AS DOUBLE)              AS measure_pct_gdp
FROM "bruegel-2026-european-energy-crisis-fiscal-response-tracker"
WHERE "Country" IS NOT NULL
