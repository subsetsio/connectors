SELECT
    id                                  AS event_id,
    CAST(time AS TIMESTAMP)             AS time,
    CAST(latitude AS DOUBLE)            AS latitude,
    CAST(longitude AS DOUBLE)           AS longitude,
    CAST(depth AS DOUBLE)               AS depth_km,
    CAST(mag AS DOUBLE)                 AS magnitude,
    CAST(magError AS DOUBLE)            AS magnitude_error,
    CAST(depthError AS DOUBLE)          AS depth_error_km,
    place,
    CAST(updated AS TIMESTAMP)          AS updated
FROM "isc-gem-earthquakes"
WHERE id IS NOT NULL
  AND time IS NOT NULL
  AND latitude IS NOT NULL
  AND longitude IS NOT NULL
  AND mag IS NOT NULL
QUALIFY row_number() OVER (PARTITION BY id ORDER BY updated DESC) = 1
