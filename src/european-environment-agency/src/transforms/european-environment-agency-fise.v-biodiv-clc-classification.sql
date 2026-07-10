SELECT
    CAST("broadleaved" AS VARCHAR) AS "broadleaved",
    CAST("broadleaved_percentage" AS VARCHAR) AS "broadleaved_percentage",
    CAST("coniferous" AS VARCHAR) AS "coniferous",
    CAST("coniferous_percentage" AS VARCHAR) AS "coniferous_percentage",
    CAST("mixed" AS VARCHAR) AS "mixed",
    CAST("mixed_percentage" AS VARCHAR) AS "mixed_percentage",
    CAST("total" AS VARCHAR) AS "total",
    CAST("transitional_woodland" AS VARCHAR) AS "transitional_woodland",
    CAST("transitional_woodland_percentage" AS VARCHAR) AS "transitional_woodland_percentage",
    CAST("units" AS VARCHAR) AS "units"
FROM "european-environment-agency-fise.v-biodiv-clc-classification"
