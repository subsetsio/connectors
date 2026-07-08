SELECT
    CAST(year AS INTEGER)               AS year,
    CAST(day_of_year AS INTEGER)        AS day_of_year,
    CAST(thirty_year_average AS DOUBLE) AS thirty_year_average
FROM "kyoto-cherry-blossom-bloom-dates"
WHERE day_of_year IS NOT NULL
ORDER BY year
