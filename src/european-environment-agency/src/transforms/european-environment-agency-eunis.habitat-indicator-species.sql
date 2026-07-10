SELECT
    CAST("code_2000" AS VARCHAR) AS "code_2000",
    CAST("habitat_unique_id" AS VARCHAR) AS "habitat_unique_id",
    CAST("id_eunis" AS VARCHAR) AS "id_eunis",
    CAST("id_habitat" AS VARCHAR) AS "id_habitat",
    CAST("picture_url" AS VARCHAR) AS "picture_url",
    CAST("relationship_code" AS VARCHAR) AS "relationship_code",
    CAST("relationship_description" AS VARCHAR) AS "relationship_description",
    CAST("scientific_name" AS VARCHAR) AS "scientific_name",
    CAST("species_group_common_name" AS VARCHAR) AS "species_group_common_name"
FROM "european-environment-agency-eunis.habitat-indicator-species"
