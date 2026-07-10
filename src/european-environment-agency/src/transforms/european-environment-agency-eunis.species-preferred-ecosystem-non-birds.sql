SELECT
    CAST("code_2000" AS VARCHAR) AS "code_2000",
    CAST("id_association" AS VARCHAR) AS "id_association",
    CAST("id_eunis" AS VARCHAR) AS "id_eunis",
    CAST("name_association" AS VARCHAR) AS "name_association",
    CAST("name_ecosystem" AS VARCHAR) AS "name_ecosystem"
FROM "european-environment-agency-eunis.species-preferred-ecosystem-non-birds"
