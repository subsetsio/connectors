SELECT
    area_code,
    area_title,
    data_type,
    method,
    period,
    TRY_CAST(REPLACE(value, ',', '') AS DOUBLE) AS value
FROM (
    UNPIVOT "connecticut-department-of-labor-nfe2-aprv"
    ON COLUMNS(* EXCLUDE (method, area_code, area_title, data_type))
    INTO NAME period VALUE value
)
WHERE TRY_CAST(REPLACE(value, ',', '') AS DOUBLE) IS NOT NULL
