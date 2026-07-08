SELECT
    try_strptime(month, '%b-%Y')::DATE AS month,
    fy AS financial_year,
    trim(state) AS state,
    trim(region) AS region,
    TRY_CAST(wind AS DOUBLE)        AS wind,
    TRY_CAST(solar AS DOUBLE)       AS solar,
    TRY_CAST(biomass AS DOUBLE)     AS biomass,
    TRY_CAST(bagasse AS DOUBLE)     AS bagasse,
    TRY_CAST(small_hydel AS DOUBLE) AS small_hydel,
    TRY_CAST(others AS DOUBLE)      AS others,
    TRY_CAST(total AS DOUBLE)       AS total
FROM "cea-india-renewable-energy"
WHERE month IS NOT NULL AND month <> ''
