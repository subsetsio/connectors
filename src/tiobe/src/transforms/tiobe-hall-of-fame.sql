SELECT
    CAST(year AS INTEGER) AS year,
    language
FROM "tiobe-hall-of-fame"
WHERE year IS NOT NULL AND language IS NOT NULL
