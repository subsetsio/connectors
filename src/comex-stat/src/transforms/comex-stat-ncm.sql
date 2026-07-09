-- comex-stat-ncm: reference/codebook table — trimmed labels, typed codes
SELECT
    "CO_NCM"                     AS ncm_code,
    CAST("CO_UNID" AS BIGINT)    AS unit_code,
    "CO_SH6"                     AS sh6_code,
    CAST("CO_PPE" AS BIGINT)     AS ppe_code,
    CAST("CO_PPI" AS BIGINT)     AS ppi_code,
    "CO_FAT_AGREG"               AS factor_aggregate_code,
    "CO_CUCI_ITEM"               AS cuci_item_code,
    CAST("CO_CGCE_N3" AS BIGINT) AS cgce_n3_code,
    CAST("CO_SIIT" AS BIGINT)    AS siit_code,
    "CO_ISIC_CLASSE"             AS isic_class_code,
    "CO_EXP_SUBSET"              AS export_subset_code,
    TRIM("NO_NCM_POR")           AS name_pt,
    TRIM("NO_NCM_ESP")           AS name_es,
    TRIM("NO_NCM_ING")           AS name_en
FROM "comex-stat-ncm"
