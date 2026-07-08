SELECT indicator_en, indicator_ar, dimension, frequency,
       year, date, period_label, value
FROM (
    SELECT *,
           row_number() OVER (
               PARTITION BY indicator_en, COALESCE(dimension, ''),
                            frequency,
                            COALESCE(CAST(date AS VARCHAR), period_label)
               ORDER BY source_file DESC
           ) AS _rn
    FROM "cbe-foreign-trade--imports-by-geographical-distribution"
    WHERE value IS NOT NULL AND indicator_en IS NOT NULL
)
WHERE _rn = 1
