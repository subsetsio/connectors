SELECT
    CO_NCM         AS ncm_code,
    CO_UNID        AS unit_code,
    CO_SH6         AS sh6_code,
    CO_PPE         AS ppe_code,
    CO_PPI         AS ppi_code,
    CO_FAT_AGREG   AS factor_aggregate_code,
    CO_CUCI_ITEM   AS cuci_item_code,
    CO_CGCE_N3     AS cgce_n3_code,
    CO_SIIT        AS siit_code,
    CO_ISIC_CLASSE AS isic_class_code,
    CO_EXP_SUBSET  AS exp_subset_code,
    NO_NCM_POR     AS name_pt,
    NO_NCM_ESP     AS name_es,
    NO_NCM_ING     AS name_en
FROM "comex-stat-ncm"
WHERE CO_NCM IS NOT NULL
