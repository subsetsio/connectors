SELECT
    CAST("annexII" AS VARCHAR) AS "annexII",
    CAST("annexIV" AS VARCHAR) AS "annexIV",
    CAST("annexV" AS VARCHAR) AS "annexV",
    CAST("assessment_speciescode" AS VARCHAR) AS "assessment_speciescode",
    CAST("assessment_speciesname" AS VARCHAR) AS "assessment_speciesname",
    CAST("country" AS VARCHAR) AS "country",
    CAST("group" AS VARCHAR) AS "group",
    CAST("presence" AS VARCHAR) AS "presence",
    CAST("priority" AS VARCHAR) AS "priority",
    CAST("region" AS VARCHAR) AS "region",
    CAST("speciescode" AS VARCHAR) AS "speciescode",
    CAST("speciesname" AS VARCHAR) AS "speciesname"
FROM "european-environment-agency-fise.n2k-art17-mastertab-species-check-list-published"
