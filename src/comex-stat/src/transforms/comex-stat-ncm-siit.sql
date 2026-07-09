-- comex-stat-ncm-siit: reference/codebook table — trimmed labels, typed codes
SELECT
    CAST("CO_SIIT" AS BIGINT) AS siit_code,
    TRIM("NO_SIIT")           AS name_pt
FROM "comex-stat-ncm-siit"
