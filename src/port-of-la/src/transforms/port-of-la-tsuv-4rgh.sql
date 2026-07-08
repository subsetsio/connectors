SELECT
    CAST(date AS DATE) AS date,
    month_year,
    TRY_CAST(monthly_total_teus AS DOUBLE) AS monthly_total_teus,
    TRY_CAST(cytd_total_teus AS DOUBLE) AS cytd_total_teus,
    TRY_CAST(previous_year_cytd AS DOUBLE) AS previous_year_cytd,
    TRY_CAST(change_total_teus_cytd AS DOUBLE) AS pct_change_total_teus_cytd
FROM "port-of-la-tsuv-4rgh"
WHERE date IS NOT NULL
