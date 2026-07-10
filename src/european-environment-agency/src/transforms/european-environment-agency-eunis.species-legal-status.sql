SELECT
    CAST("code_2000" AS VARCHAR) AS "code_2000",
    CAST("dc_index_reference_title" AS VARCHAR) AS "dc_index_reference_title",
    CAST("dc_index_title" AS VARCHAR) AS "dc_index_title",
    CAST("dc_index_url" AS VARCHAR) AS "dc_index_url",
    CAST("id_dc" AS VARCHAR) AS "id_dc",
    CAST("id_eunis" AS VARCHAR) AS "id_eunis",
    CAST("legal_status_comment" AS VARCHAR) AS "legal_status_comment"
FROM "european-environment-agency-eunis.species-legal-status"
