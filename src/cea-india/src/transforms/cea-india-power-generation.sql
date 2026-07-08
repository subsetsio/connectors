SELECT
    try_strptime(month, '%b-%Y')::DATE AS month,
    fy AS financial_year,
    trim(mode) AS mode,
    TRY_CAST(bus AS DOUBLE) AS bus_energy
FROM "cea-india-power-generation"
WHERE month IS NOT NULL AND month <> ''
