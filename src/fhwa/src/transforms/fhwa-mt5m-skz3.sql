SELECT
    CAST(year AS INTEGER)                               AS year,
    state                                               AS state,
    TRY_CAST(vehicles_weighed_fixed AS BIGINT)          AS vehicles_weighed_fixed_scale,
    TRY_CAST(vehicles_weighed_wim AS BIGINT)            AS vehicles_weighed_wim_scale,
    TRY_CAST(vehicles_weighed_portable AS BIGINT)       AS vehicles_weighed_portable_scale,
    TRY_CAST(vehicles_weighed_semi_portable AS BIGINT)  AS vehicles_weighed_semi_portable_scale,
    TRY_CAST(oversize_violation_current_year AS BIGINT) AS oversize_violations,
    TRY_CAST(overweight_violation_current_year AS BIGINT) AS overweight_violations,
    TRY_CAST(non_divisible_trip_permits AS BIGINT)      AS non_divisible_trip_permits,
    TRY_CAST(non_divisible_annual_permits AS BIGINT)    AS non_divisible_annual_permits,
    TRY_CAST(divisible_trip_permits AS BIGINT)          AS divisible_trip_permits,
    TRY_CAST(divisible_annual_permits AS BIGINT)        AS divisible_annual_permits
FROM "fhwa-mt5m-skz3"
WHERE year IS NOT NULL AND state IS NOT NULL
  AND TRY_CAST(year AS INTEGER) IS NOT NULL
