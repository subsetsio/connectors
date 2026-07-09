-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: One row per announced national fiscal measure. There is no null-free row identity: Country + Date Announced + Measure Name separates every row, but the workbook ships measures with no name, so the table is published keyless. Amounts are pre-converted to euros; Measure in % of GDP is that measure's cost against its own country's GDP, so summing it across countries is misleading.
SELECT
    "Country" AS country,
    "Date Announced" AS date_announced,
    "Time Horizon" AS time_horizon,
    "Status" AS status,
    "Measure Name" AS measure_name,
    "Details" AS details,
    "Total Amount (in millions in local currency)" AS total_amount_in_millions_in_local_currency,
    "Currency / Unit" AS currency_unit,
    "Total Amount (in billion euros)" AS total_amount_in_billion_euros,
    "Total Amount (in million euros)" AS total_amount_in_million_euros,
    "Broad Measure Type" AS broad_measure_type,
    "Specific Measure Type" AS specific_measure_type,
    "Energy carrier" AS energy_carrier,
    "Target Group" AS target_group,
    "Change in incentives to consume fossil fuels" AS change_in_incentives_to_consume_fossil_fuels,
    "Government Source" AS government_source,
    "English Source" AS english_source,
    "GDP (in billion euros)" AS gdp_in_billion_euros,
    "GDP (in million euros)" AS gdp_in_million_euros,
    "Measure in % of GDP" AS measure_in_of_gdp
FROM "bruegel-2026-european-energy-crisis-fiscal-response-tracker"
