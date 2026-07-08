SELECT series, period, year, part, CAST(date AS DATE) AS date, value
FROM "monetary-authority-of-macao-2-resident-deps-and-domestic-credit--resident-time-deposits"
WHERE value IS NOT NULL
QUALIFY row_number() OVER (
    PARTITION BY series, period, part ORDER BY value DESC
) = 1
