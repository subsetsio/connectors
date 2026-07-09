-- comex-stat-ncm-isic: reference/codebook table — trimmed labels, typed codes
SELECT
    "CO_ISIC_CLASSE"            AS isic_class_code,
    TRIM("NO_ISIC_CLASSE")      AS isic_class_name_pt,
    TRIM("NO_ISIC_CLASSE_ING")  AS isic_class_name_en,
    TRIM("NO_ISIC_CLASSE_ESP")  AS isic_class_name_es,
    "CO_ISIC_GRUPO"             AS isic_group_code,
    TRIM("NO_ISIC_GRUPO")       AS isic_group_name_pt,
    TRIM("NO_ISIC_GRUPO_ING")   AS isic_group_name_en,
    TRIM("NO_ISIC_GRUPO_ESP")   AS isic_group_name_es,
    "CO_ISIC_DIVISAO"           AS isic_division_code,
    TRIM("NO_ISIC_DIVISAO")     AS isic_division_name_pt,
    TRIM("NO_ISIC_DIVISAO_ING") AS isic_division_name_en,
    TRIM("NO_ISIC_DIVISAO_ESP") AS isic_division_name_es,
    "CO_ISIC_SECAO"             AS isic_section_code,
    TRIM("NO_ISIC_SECAO")       AS isic_section_name_pt,
    TRIM("NO_ISIC_SECAO_ING")   AS isic_section_name_en,
    TRIM("NO_ISIC_SECAO_ESP")   AS isic_section_name_es
FROM "comex-stat-ncm-isic"
