SELECT
    CAST("country_code" AS VARCHAR) AS "country_code",
    CAST("country_name" AS VARCHAR) AS "country_name",
    CAST("number_cdda_sites" AS VARCHAR) AS "number_cdda_sites",
    CAST("number_habitats" AS VARCHAR) AS "number_habitats",
    CAST("number_natura2000_sites" AS VARCHAR) AS "number_natura2000_sites",
    CAST("number_natura2000_sites_birds_directive" AS VARCHAR) AS "number_natura2000_sites_birds_directive",
    CAST("number_natura2000_sites_habitats_directive" AS VARCHAR) AS "number_natura2000_sites_habitats_directive",
    CAST("number_species" AS VARCHAR) AS "number_species",
    CAST("number_species_birds_directive" AS VARCHAR) AS "number_species_birds_directive",
    CAST("number_species_habitats_directive" AS VARCHAR) AS "number_species_habitats_directive",
    CAST("number_total_sites" AS VARCHAR) AS "number_total_sites"
FROM "european-environment-agency-bise.v-country-information"
