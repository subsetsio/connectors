SELECT
    CAST(year AS VARCHAR) AS year,
    CAST(constellation AS VARCHAR) AS constellation,
    CAST(category AS VARCHAR) AS category,
    CAST(launched_that_year AS BIGINT) AS launched_that_year,
    CAST(cumulative_total AS BIGINT) AS cumulative_total,
    CAST(active_count AS BIGINT) AS active_count
FROM "celestrak-constellation-growth"
