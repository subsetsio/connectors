-- comex-stat-uf: reference/codebook table — trimmed labels, typed codes
SELECT
    CAST("CO_UF" AS BIGINT) AS state_code,
    TRIM("SG_UF")           AS state_abbr,
    TRIM("NO_UF")           AS name_pt,
    TRIM("NO_REGIAO")       AS region_pt
FROM "comex-stat-uf"
