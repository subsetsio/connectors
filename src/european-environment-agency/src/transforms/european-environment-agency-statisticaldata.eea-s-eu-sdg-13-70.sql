SELECT
    CAST("dimension" AS VARCHAR) AS "dimension",
    CAST("dimension_label" AS VARCHAR) AS "dimension_label",
    CAST("eu_sdg" AS VARCHAR) AS "eu_sdg",
    CAST("geo" AS VARCHAR) AS "geo",
    CAST("geo_label" AS VARCHAR) AS "geo_label",
    CAST("obs_status" AS VARCHAR) AS "obs_status",
    CAST("obs_value" AS VARCHAR) AS "obs_value",
    CAST("time" AS VARCHAR) AS "time",
    CAST("unit" AS VARCHAR) AS "unit",
    CAST("unit_label" AS VARCHAR) AS "unit_label"
FROM "european-environment-agency-statisticaldata.eea-s-eu-sdg-13-70"
