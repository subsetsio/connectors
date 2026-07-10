SELECT
    CAST("area_with_number_of_tree_species_occurring_1" AS VARCHAR) AS "area_with_number_of_tree_species_occurring_1",
    CAST("area_with_number_of_tree_species_occurring_2_3" AS VARCHAR) AS "area_with_number_of_tree_species_occurring_2_3",
    CAST("area_with_number_of_tree_species_occurring_4_5" AS VARCHAR) AS "area_with_number_of_tree_species_occurring_4_5",
    CAST("area_with_number_of_tree_species_occurring_6_pl" AS VARCHAR) AS "area_with_number_of_tree_species_occurring_6_pl",
    CAST("country" AS VARCHAR) AS "country",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("perct_1" AS VARCHAR) AS "perct_1",
    CAST("perct_2_3" AS VARCHAR) AS "perct_2_3",
    CAST("perct_2_5" AS VARCHAR) AS "perct_2_5",
    CAST("perct_4_5" AS VARCHAR) AS "perct_4_5",
    CAST("perct_6_pl" AS VARCHAR) AS "perct_6_pl",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.v-biodiv-soef20-tree-species-occurring"
