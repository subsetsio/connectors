SELECT
    item_name,
    reference_period,
    CAST(p10 AS DOUBLE)    AS p10,
    CAST(p25 AS DOUBLE)    AS p25,
    CAST(median AS DOUBLE) AS median,
    CAST(p75 AS DOUBLE)    AS p75,
    CAST(p90 AS DOUBLE)    AS p90,
    TRY_CAST(n_observations AS BIGINT) AS n_observations
FROM "eiopa-financial-stability-indicators"
WHERE median IS NOT NULL
