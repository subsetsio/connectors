SELECT
    CAST("amount" AS VARCHAR) AS "amount",
    CAST("country" AS VARCHAR) AS "country",
    CAST("for_acc" AS VARCHAR) AS "for_acc",
    CAST("unit" AS VARCHAR) AS "unit",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.eurostat-economic-output"
