-- comex-stat-isic-cuci: reference/codebook table — trimmed labels, typed codes
SELECT
    "CO_ISIC_SECAO"       AS isic_section_code,
    TRIM("NO_ISIC_SECAO") AS isic_section_name_pt,
    "CO_CUCI_GRUPO"       AS cuci_group_code,
    TRIM("NO_CUCI_GRUPO") AS cuci_group_name_pt
FROM "comex-stat-isic-cuci"
