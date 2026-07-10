SELECT
    CAST("code_2000" AS VARCHAR) AS "code_2000",
    CAST("english_name" AS VARCHAR) AS "english_name",
    CAST("eunis_habitat_code" AS VARCHAR) AS "eunis_habitat_code",
    CAST("habitat_category" AS VARCHAR) AS "habitat_category",
    CAST("habitat_description" AS VARCHAR) AS "habitat_description",
    CAST("habitat_type_tree" AS VARCHAR) AS "habitat_type_tree",
    CAST("habitat_unique_id" AS VARCHAR) AS "habitat_unique_id",
    CAST("id_dc" AS VARCHAR) AS "id_dc",
    CAST("id_habitat" AS VARCHAR) AS "id_habitat",
    CAST("priority" AS VARCHAR) AS "priority",
    CAST("scientific_name" AS VARCHAR) AS "scientific_name",
    CAST("scientific_name_clean" AS VARCHAR) AS "scientific_name_clean",
    CAST("SEA_NAME" AS VARCHAR) AS "SEA_NAME"
FROM "european-environment-agency-eunis.habitat-information"
