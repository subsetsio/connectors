SELECT
    CAST("amount" AS VARCHAR) AS "amount",
    CAST("country" AS VARCHAR) AS "country",
    CAST("statinfo" AS VARCHAR) AS "statinfo",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.eurostat-env-bio3"
