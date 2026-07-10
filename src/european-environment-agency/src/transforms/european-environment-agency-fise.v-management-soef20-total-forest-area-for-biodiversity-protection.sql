SELECT
    CAST("forest_area_within_protected_areas" AS VARCHAR) AS "forest_area_within_protected_areas",
    CAST("mcpfe_1_total" AS VARCHAR) AS "mcpfe_1_total",
    CAST("mcpfe_class_1_1" AS VARCHAR) AS "mcpfe_class_1_1",
    CAST("mcpfe_class_1_1_perct" AS VARCHAR) AS "mcpfe_class_1_1_perct",
    CAST("mcpfe_class_1_2" AS VARCHAR) AS "mcpfe_class_1_2",
    CAST("mcpfe_class_1_2_perct" AS VARCHAR) AS "mcpfe_class_1_2_perct",
    CAST("mcpfe_class_1_3" AS VARCHAR) AS "mcpfe_class_1_3",
    CAST("mcpfe_class_1_3_perct" AS VARCHAR) AS "mcpfe_class_1_3_perct",
    CAST("mcpfe_class_2" AS VARCHAR) AS "mcpfe_class_2",
    CAST("mcpfe_class_2_perct" AS VARCHAR) AS "mcpfe_class_2_perct",
    CAST("mcpfe_total" AS VARCHAR) AS "mcpfe_total",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("share_protected_forests_class_1" AS VARCHAR) AS "share_protected_forests_class_1",
    CAST("share_protected_forests_total" AS VARCHAR) AS "share_protected_forests_total",
    CAST("total_forest_area" AS VARCHAR) AS "total_forest_area",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.v-management-soef20-total-forest-area-for-biodiversity-protection"
