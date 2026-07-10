SELECT
    CAST("available_for_wood_supply_of_which" AS VARCHAR) AS "available_for_wood_supply_of_which",
    CAST("country" AS VARCHAR) AS "country",
    CAST("forest_even_aged_stands_of_which" AS VARCHAR) AS "forest_even_aged_stands_of_which",
    CAST("mixed_forest" AS VARCHAR) AS "mixed_forest",
    CAST("predominantly_broadleaved_forest" AS VARCHAR) AS "predominantly_broadleaved_forest",
    CAST("predominantly_coniferous_forest" AS VARCHAR) AS "predominantly_coniferous_forest",
    CAST("variable" AS VARCHAR) AS "variable",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.v-nat-soef20-forest-aged"
