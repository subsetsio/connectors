SELECT
    CO_PAIS       AS country_code,
    CO_PAIS_ISON3 AS iso_numeric_code,
    CO_PAIS_ISOA3 AS iso_alpha3_code,
    NO_PAIS       AS name_pt,
    NO_PAIS_ING   AS name_en,
    NO_PAIS_ESP   AS name_es
FROM "comex-stat-pais"
WHERE CO_PAIS IS NOT NULL
