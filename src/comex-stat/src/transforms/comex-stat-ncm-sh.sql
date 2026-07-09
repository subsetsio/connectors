-- comex-stat-ncm-sh: reference/codebook table — trimmed labels, typed codes
SELECT
    "CO_SH6"           AS sh6_code,
    TRIM("NO_SH6_POR") AS sh6_name_pt,
    TRIM("NO_SH6_ESP") AS sh6_name_es,
    TRIM("NO_SH6_ING") AS sh6_name_en,
    "CO_SH4"           AS sh4_code,
    TRIM("NO_SH4_POR") AS sh4_name_pt,
    TRIM("NO_SH4_ESP") AS sh4_name_es,
    TRIM("NO_SH4_ING") AS sh4_name_en,
    "CO_SH2"           AS sh2_code,
    TRIM("NO_SH2_POR") AS sh2_name_pt,
    TRIM("NO_SH2_ESP") AS sh2_name_es,
    TRIM("NO_SH2_ING") AS sh2_name_en,
    "CO_NCM_SECROM"    AS section_code,
    TRIM("NO_SEC_POR") AS section_name_pt,
    TRIM("NO_SEC_ESP") AS section_name_es,
    TRIM("NO_SEC_ING") AS section_name_en
FROM "comex-stat-ncm-sh"
