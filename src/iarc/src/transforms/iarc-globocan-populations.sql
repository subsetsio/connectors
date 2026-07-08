SELECT
    CAST(country_code AS BIGINT)  AS country_code,
    CAST(label AS VARCHAR)        AS label,
    CAST(country_iso3 AS VARCHAR) AS iso3,
    CAST(continent_code AS VARCHAR) AS continent_code,
    CAST(area_label AS VARCHAR)   AS area_label,
    CAST(grouping AS VARCHAR)     AS grouping,
    TRY_CAST(hdi_value AS DOUBLE) AS hdi_value,
    CAST(hdi_label AS VARCHAR)    AS hdi_label,
    CAST(income_label AS VARCHAR) AS income_label,
    CAST(who_region AS VARCHAR)   AS who_region,
    CAST(who_label AS VARCHAR)    AS who_label
FROM "iarc-globocan-populations"
WHERE country_code IS NOT NULL
