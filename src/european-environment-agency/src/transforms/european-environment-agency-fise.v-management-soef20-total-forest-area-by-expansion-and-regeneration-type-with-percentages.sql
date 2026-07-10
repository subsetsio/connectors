SELECT
    CAST("afforestation_and_regeneration_by_planting_and_or_seeding" AS VARCHAR) AS "afforestation_and_regeneration_by_planting_and_or_seeding",
    CAST("afforestation_and_regeneration_by_planting_and_or_seeding_percentage" AS VARCHAR) AS "afforestation_and_regeneration_by_planting_and_or_seeding_percentage",
    CAST("Coppice" AS VARCHAR) AS "Coppice",
    CAST("coppice_percentage" AS VARCHAR) AS "coppice_percentage",
    CAST("country" AS VARCHAR) AS "country",
    CAST("natural_expansion_and_natural_regeneration" AS VARCHAR) AS "natural_expansion_and_natural_regeneration",
    CAST("natural_expansion_and_natural_regeneration_percentage" AS VARCHAR) AS "natural_expansion_and_natural_regeneration_percentage",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("total" AS VARCHAR) AS "total",
    CAST("units" AS VARCHAR) AS "units",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.v-management-soef20-total-forest-area-by-expansion-and-regeneration-type-with-percentages"
