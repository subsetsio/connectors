SELECT
    try_strptime(month, '%b-%Y')::DATE AS month,
    fy AS financial_year,
    trim(state) AS state,
    TRY_CAST(energy_requirement AS DOUBLE)  AS energy_requirement_mu,
    TRY_CAST(energy_availability AS DOUBLE) AS energy_availability_mu
FROM "cea-india-psp-energy"
WHERE month IS NOT NULL AND month <> ''
