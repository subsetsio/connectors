SELECT
    reporting_unit_code,
    reporting_unit_name,
    reporting_unit_type_code,
    reporting_unit_type_name,
    TRY_CAST(latitude AS DOUBLE)  AS latitude,
    TRY_CAST(longitude AS DOUBLE) AS longitude,
    CAST(closed AS BOOLEAN)       AS closed,
    CAST(private AS BOOLEAN)      AS private
FROM "aihw-reporting-units"
WHERE reporting_unit_code IS NOT NULL
