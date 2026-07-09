SELECT
    strptime("date", '%Y-%m-%d')::DATE AS date,
    CASE WHEN isnan("median_pce_inflation_monthly_percent_change") THEN NULL
         ELSE "median_pce_inflation_monthly_percent_change" END AS monthly_percent_change,
    CASE WHEN isnan("median_pce_inflation_year_over_year_percent_change") THEN NULL
         ELSE "median_pce_inflation_year_over_year_percent_change" END AS year_over_year_percent_change
FROM "cleveland-fed-medianpce-median-pce-full-history"
WHERE NOT (isnan("median_pce_inflation_monthly_percent_change")
           AND isnan("median_pce_inflation_year_over_year_percent_change"))
