-- comex-stat-ncm-ppe: reference/codebook table — trimmed labels, typed codes
SELECT
    CAST("CO_PPE" AS BIGINT) AS ppe_code,
    TRIM("NO_PPE")           AS name_pt,
    TRIM("NO_PPE_MIN")       AS name_pt_short,
    TRIM("NO_PPE_ING")       AS name_en
FROM "comex-stat-ncm-ppe"
