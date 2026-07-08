SELECT
    office_code,
    publishing_office,
    CAST(report_datetime AS TIMESTAMPTZ) AS report_datetime,
    area_code, area_name, element,
    CAST(valid_time AS TIMESTAMPTZ) AS valid_time,
    value
FROM "japan-meteorological-agency-weather-forecasts"
WHERE area_code IS NOT NULL AND element IS NOT NULL AND valid_time IS NOT NULL
