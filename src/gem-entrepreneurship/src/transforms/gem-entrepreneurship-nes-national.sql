SELECT
    CAST(year AS INTEGER) AS year,
    CAST(economy_code AS BIGINT) AS economy_code,
    CAST(economy_name AS VARCHAR) AS economy_name,
    CAST(economy_iso AS VARCHAR) AS economy_iso,
    CAST(indicator AS VARCHAR) AS indicator,
    CAST(variable AS VARCHAR) AS variable,
    CAST(label AS VARCHAR) AS label,
    CAST(value AS DOUBLE) AS value
FROM "gem-entrepreneurship-nes-national"
WHERE value IS NOT NULL
  AND indicator IS NOT NULL
