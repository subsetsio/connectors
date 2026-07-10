SELECT
    CAST("country" AS VARCHAR) AS "country",
    CAST("featurecode" AS VARCHAR) AS "featurecode",
    CAST("featurename" AS VARCHAR) AS "featurename",
    CAST("featuretype" AS VARCHAR) AS "featuretype",
    CAST("pressurecode" AS VARCHAR) AS "pressurecode",
    CAST("ranking" AS VARCHAR) AS "ranking",
    CAST("region" AS VARCHAR) AS "region",
    CAST("type" AS VARCHAR) AS "type",
    CAST("use_for_statistics" AS VARCHAR) AS "use_for_statistics"
FROM "european-environment-agency-fise.n2k-art17-mastertab-data-pressures-threats-published"
