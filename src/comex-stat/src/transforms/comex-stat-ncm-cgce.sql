-- comex-stat-ncm-cgce: reference/codebook table — trimmed labels, typed codes
SELECT
    CAST("CO_CGCE_N3" AS BIGINT) AS cgce_n3_code,
    TRIM("NO_CGCE_N3")           AS cgce_n3_name_pt,
    TRIM("NO_CGCE_N3_ING")       AS cgce_n3_name_en,
    TRIM("NO_CGCE_N3_ESP")       AS cgce_n3_name_es,
    CAST("CO_CGCE_N2" AS BIGINT) AS cgce_n2_code,
    TRIM("NO_CGCE_N2")           AS cgce_n2_name_pt,
    TRIM("NO_CGCE_N2_ING")       AS cgce_n2_name_en,
    TRIM("NO_CGCE_N2_ESP")       AS cgce_n2_name_es,
    CAST("CO_CGCE_N1" AS BIGINT) AS cgce_n1_code,
    TRIM("NO_CGCE_N1")           AS cgce_n1_name_pt,
    TRIM("NO_CGCE_N1_ING")       AS cgce_n1_name_en,
    TRIM("NO_CGCE_N1_ESP")       AS cgce_n1_name_es
FROM "comex-stat-ncm-cgce"
