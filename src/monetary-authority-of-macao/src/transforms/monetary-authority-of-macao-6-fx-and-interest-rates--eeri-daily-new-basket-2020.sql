SELECT series, period, year, part, CAST(date AS DATE) AS date, value
FROM "monetary-authority-of-macao-6-fx-and-interest-rates--eeri-daily-new-basket-2020"
WHERE value IS NOT NULL
QUALIFY row_number() OVER (
    PARTITION BY series, period, part ORDER BY value DESC
) = 1
