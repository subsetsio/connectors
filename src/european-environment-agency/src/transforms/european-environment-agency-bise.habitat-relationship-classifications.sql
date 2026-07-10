SELECT
    CAST("classification" AS VARCHAR) AS "classification",
    CAST("code" AS VARCHAR) AS "code",
    CAST("code_2000" AS VARCHAR) AS "code_2000",
    CAST("name" AS VARCHAR) AS "name",
    CAST("relation_type_name" AS VARCHAR) AS "relation_type_name"
FROM "european-environment-agency-bise.habitat-relationship-classifications"
