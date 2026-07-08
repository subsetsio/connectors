SELECT
    language,
    CAST(snapshot_year AS INTEGER) AS snapshot_year,
    CAST(position AS INTEGER)      AS position
FROM "tiobe-very-long-term-history"
WHERE position IS NOT NULL AND language IS NOT NULL
