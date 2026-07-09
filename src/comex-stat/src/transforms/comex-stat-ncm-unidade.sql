-- comex-stat-ncm-unidade: reference/codebook table — trimmed labels, typed codes
SELECT
    CAST("CO_UNID" AS BIGINT) AS unit_code,
    TRIM("NO_UNID")           AS name_pt,
    TRIM("SG_UNID")           AS abbreviation
FROM "comex-stat-ncm-unidade"
