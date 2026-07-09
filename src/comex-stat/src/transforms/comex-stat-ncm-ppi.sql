-- comex-stat-ncm-ppi: reference/codebook table — trimmed labels, typed codes
SELECT
    CAST("CO_PPI" AS BIGINT) AS ppi_code,
    TRIM("NO_PPI")           AS name_pt,
    TRIM("NO_PPI_MIN")       AS name_pt_short,
    TRIM("NO_PPI_ING")       AS name_en
FROM "comex-stat-ncm-ppi"
