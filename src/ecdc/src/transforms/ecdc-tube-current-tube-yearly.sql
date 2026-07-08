SELECT DISTINCT
    health_topic,
    population,
    indicator,
    unit,
    geo_level,
    time_unit,
    time,
    region_code,
    region_name,
    CAST(num_value AS DOUBLE) AS num_value,
    txt_value
FROM "ecdc-tube-current-tube-yearly"
WHERE num_value IS NOT NULL OR txt_value IS NOT NULL
