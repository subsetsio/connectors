SELECT
    CAST("author" AS VARCHAR) AS "author",
    CAST("code_2000" AS VARCHAR) AS "code_2000",
    CAST("common_name" AS VARCHAR) AS "common_name",
    CAST("common_name_list" AS VARCHAR) AS "common_name_list",
    CAST("id_eunis" AS VARCHAR) AS "id_eunis",
    CAST("number_countries" AS VARCHAR) AS "number_countries",
    CAST("number_sites" AS VARCHAR) AS "number_sites",
    CAST("picture_url" AS VARCHAR) AS "picture_url",
    CAST("scientific_name" AS VARCHAR) AS "scientific_name",
    CAST("species_group_name" AS VARCHAR) AS "species_group_name",
    CAST("threat_code_E27" AS VARCHAR) AS "threat_code_E27",
    CAST("threat_code_EU" AS VARCHAR) AS "threat_code_EU",
    CAST("threat_code_WO" AS VARCHAR) AS "threat_code_WO",
    CAST("threat_name_E27" AS VARCHAR) AS "threat_name_E27",
    CAST("threat_name_EU" AS VARCHAR) AS "threat_name_EU",
    CAST("threat_name_WO" AS VARCHAR) AS "threat_name_WO"
FROM "european-environment-agency-bise.species-information"
