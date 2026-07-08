PIVOT (
    SELECT date, metric, value
    FROM "ism-pmi"
    WHERE value IS NOT NULL
)
ON metric
USING first(value)
GROUP BY date
ORDER BY date
