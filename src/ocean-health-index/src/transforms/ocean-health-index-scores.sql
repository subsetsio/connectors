SELECT
    scenario AS year,
    goal,
    long_goal,
    dimension,
    region_id,
    region_name,
    CAST(value AS DOUBLE) AS value
FROM "ocean-health-index-scores"
