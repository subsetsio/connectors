SELECT
    CAST(position AS INTEGER)  AS position,
    language,
    CAST(rating_pct AS DOUBLE) AS rating_pct
FROM "tiobe-next-50-languages"
WHERE position IS NOT NULL AND language IS NOT NULL
