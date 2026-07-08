SELECT
    try_strptime(month, '%b-%Y')::DATE AS month,
    fy AS financial_year,
    trim(state) AS state,
    TRY_CAST(peak_demand AS DOUBLE) AS peak_demand_mw,
    TRY_CAST(peak_met AS DOUBLE)    AS peak_met_mw
FROM "cea-india-psp-peak"
WHERE month IS NOT NULL AND month <> ''
