SELECT
    CAST("countryCode" AS VARCHAR) AS "countryCode",
    CAST("countryName" AS VARCHAR) AS "countryName",
    CAST("differenceBetween2016And2006" AS VARCHAR) AS "differenceBetween2016And2006",
    CAST("discodataUpdate" AS VARCHAR) AS "discodataUpdate",
    CAST("remediated2006" AS VARCHAR) AS "remediated2006",
    CAST("remediated2016" AS VARCHAR) AS "remediated2016"
FROM "european-environment-agency-bise.kcbd-remediated-sites-2006-2016-in-europe"
