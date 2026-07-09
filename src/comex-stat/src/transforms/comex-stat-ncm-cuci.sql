-- comex-stat-ncm-cuci: reference/codebook table — trimmed labels, typed codes
SELECT
    "CO_CUCI_ITEM"                AS cuci_item_code,
    TRIM("NO_CUCI_ITEM")          AS cuci_item_name_pt,
    "CO_CUCI_SUB"                 AS cuci_subgroup_code,
    TRIM("NO_CUCI_SUB")           AS cuci_subgroup_name_pt,
    "CO_CUCI_GRUPO"               AS cuci_group_code,
    TRIM("NO_CUCI_GRUPO")         AS cuci_group_name_pt,
    "CO_CUCI_DIVISAO"             AS cuci_division_code,
    TRIM("NO_CUCI_DIVISAO")       AS cuci_division_name_pt,
    CAST("CO_CUCI_SEC" AS BIGINT) AS cuci_section_code,
    TRIM("NO_CUCI_SEC")           AS cuci_section_name_pt
FROM "comex-stat-ncm-cuci"
