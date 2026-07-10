SELECT
    CAST("country" AS VARCHAR) AS "country",
    CAST("diseases" AS VARCHAR) AS "diseases",
    CAST("insects" AS VARCHAR) AS "insects",
    CAST("NUTS_CODE" AS VARCHAR) AS "NUTS_CODE",
    CAST("other" AS VARCHAR) AS "other",
    CAST("severe_weather_events" AS VARCHAR) AS "severe_weather_events",
    CAST("total" AS VARCHAR) AS "total",
    CAST("units" AS VARCHAR) AS "units",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.v-vita-gfra-disturbances"
