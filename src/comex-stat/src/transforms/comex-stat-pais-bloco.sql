-- comex-stat-pais-bloco: reference/codebook table — trimmed labels, typed codes
SELECT
    "CO_PAIS"                  AS country_code,
    CAST("CO_BLOCO" AS BIGINT) AS bloc_code,
    TRIM("NO_BLOCO")           AS bloc_name_pt,
    TRIM("NO_BLOCO_ING")       AS bloc_name_en,
    TRIM("NO_BLOCO_ESP")       AS bloc_name_es
FROM "comex-stat-pais-bloco"
