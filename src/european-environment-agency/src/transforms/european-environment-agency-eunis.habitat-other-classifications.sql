SELECT
    CAST("classification" AS VARCHAR) AS "classification",
    CAST("code" AS VARCHAR) AS "code",
    CAST("habitat_type_name" AS VARCHAR) AS "habitat_type_name",
    CAST("habitat_unique_id" AS VARCHAR) AS "habitat_unique_id",
    CAST("id_dc" AS VARCHAR) AS "id_dc",
    CAST("id_habitat" AS VARCHAR) AS "id_habitat",
    CAST("relation_type_code" AS VARCHAR) AS "relation_type_code",
    CAST("relation_type_name" AS VARCHAR) AS "relation_type_name",
    CAST("sort_order" AS VARCHAR) AS "sort_order"
FROM "european-environment-agency-eunis.habitat-other-classifications"
