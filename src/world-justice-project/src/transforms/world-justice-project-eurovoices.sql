SELECT
    country,
    level,
    region_name,
    nuts_id,
    report,
    chapter,
    chapter_number,
    topic_number,
    topic,
    subtitle,
    CAST(score AS DOUBLE) AS score
FROM "world-justice-project-eurovoices"
WHERE score IS NOT NULL
  AND country IS NOT NULL
