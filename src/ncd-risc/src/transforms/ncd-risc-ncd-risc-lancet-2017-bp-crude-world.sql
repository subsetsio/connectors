SELECT
    CAST(area AS VARCHAR)   AS area,
    CAST(iso AS VARCHAR)    AS iso,
    CAST(sex AS VARCHAR)    AS sex,
    CAST(year AS INTEGER)   AS year,
    CAST(age AS VARCHAR)    AS age,
    CAST(metric AS VARCHAR) AS metric,
    CAST(value AS DOUBLE)   AS value
FROM "ncd-risc-ncd-risc-lancet-2017-bp-crude-world"
WHERE value IS NOT NULL
