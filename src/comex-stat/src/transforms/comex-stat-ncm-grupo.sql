-- comex-stat-ncm-grupo: reference/codebook table — trimmed labels, typed codes
SELECT
    "CO_EXP_SUBSET"           AS export_subset_code,
    TRIM("NO_EXP_SUBSET_POR") AS subset_name_pt,
    TRIM("NO_EXP_SUBSET_ESP") AS subset_name_es,
    TRIM("NO_EXP_SUBSET_ING") AS subset_name_en,
    "CO_EXP_SET"              AS export_set_code,
    TRIM("NO_EXP_SET")        AS set_name_pt,
    TRIM("NO_EXP_SET_ESP")    AS set_name_es,
    TRIM("NO_EXP_SET_ING")    AS set_name_en
FROM "comex-stat-ncm-grupo"
