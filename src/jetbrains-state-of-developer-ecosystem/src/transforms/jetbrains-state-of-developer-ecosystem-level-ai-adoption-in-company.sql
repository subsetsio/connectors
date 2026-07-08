SELECT category, series, unit, value
FROM (
    SELECT
        label                  AS category,
        "group"                AS series,
        unit                   AS unit,
        CAST(value AS DOUBLE)  AS value,
        row_number() OVER (
            PARTITION BY label, "group"
            ORDER BY value DESC
        ) AS rn
    FROM "jetbrains-state-of-developer-ecosystem-level-ai-adoption-in-company"
    WHERE value IS NOT NULL AND label IS NOT NULL
)
WHERE rn = 1
