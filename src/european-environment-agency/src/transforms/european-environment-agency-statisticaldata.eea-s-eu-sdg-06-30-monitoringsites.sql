SELECT
    CAST("code" AS VARCHAR) AS "code",
    CAST("GEO_Codes" AS VARCHAR) AS "GEO_Codes",
    CAST("GEO_Labels" AS VARCHAR) AS "GEO_Labels",
    CAST("number_of_water_bodies" AS VARCHAR) AS "number_of_water_bodies"
FROM "european-environment-agency-statisticaldata.eea-s-eu-sdg-06-30-monitoringsites"
