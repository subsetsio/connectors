-- comex-stat-pais: reference/codebook table — trimmed labels, typed codes
SELECT
    "CO_PAIS"           AS country_code,
    "CO_PAIS_ISON3"     AS iso_numeric,
    "CO_PAIS_ISOA3"     AS iso_alpha3,
    TRIM("NO_PAIS")     AS name_pt,
    TRIM("NO_PAIS_ING") AS name_en,
    TRIM("NO_PAIS_ESP") AS name_es
FROM "comex-stat-pais"
