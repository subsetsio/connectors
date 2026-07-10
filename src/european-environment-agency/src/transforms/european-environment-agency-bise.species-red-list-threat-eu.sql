SELECT
    CAST("id_eunis" AS VARCHAR) AS "id_eunis",
    CAST("threat_code" AS VARCHAR) AS "threat_code",
    CAST("threat_name" AS VARCHAR) AS "threat_name"
FROM "european-environment-agency-bise.species-red-list-threat-eu"
