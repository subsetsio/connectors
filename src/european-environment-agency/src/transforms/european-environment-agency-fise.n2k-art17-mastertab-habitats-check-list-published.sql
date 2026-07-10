SELECT
    CAST("country" AS VARCHAR) AS "country",
    CAST("group" AS VARCHAR) AS "group",
    CAST("habitatcode" AS VARCHAR) AS "habitatcode",
    CAST("habitatname" AS VARCHAR) AS "habitatname",
    CAST("presence" AS VARCHAR) AS "presence",
    CAST("priority" AS VARCHAR) AS "priority",
    CAST("region" AS VARCHAR) AS "region"
FROM "european-environment-agency-fise.n2k-art17-mastertab-habitats-check-list-published"
