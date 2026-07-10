SELECT
    CAST("code_legal_text" AS VARCHAR) AS "code_legal_text",
    CAST("dc_reference_title" AS VARCHAR) AS "dc_reference_title",
    CAST("dc_reference_url" AS VARCHAR) AS "dc_reference_url",
    CAST("dc_title" AS VARCHAR) AS "dc_title",
    CAST("habitat_unique_id" AS VARCHAR) AS "habitat_unique_id",
    CAST("id_dc" AS VARCHAR) AS "id_dc",
    CAST("id_habitat" AS VARCHAR) AS "id_habitat",
    CAST("info_url" AS VARCHAR) AS "info_url",
    CAST("name_legal_text" AS VARCHAR) AS "name_legal_text",
    CAST("relation_type_name" AS VARCHAR) AS "relation_type_name"
FROM "european-environment-agency-eunis.habitat-legal-status-relation-other-habitats"
