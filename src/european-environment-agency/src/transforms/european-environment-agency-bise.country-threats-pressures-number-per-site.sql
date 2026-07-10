SELECT
    CAST("country_code" AS VARCHAR) AS "country_code",
    CAST("number_threats_pressures" AS VARCHAR) AS "number_threats_pressures",
    CAST("site_name" AS VARCHAR) AS "site_name"
FROM "european-environment-agency-bise.country-threats-pressures-number-per-site"
