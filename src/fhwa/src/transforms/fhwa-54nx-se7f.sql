SELECT
    CAST(year AS INTEGER)              AS year,
    TRY_CAST(roadmiles AS BIGINT)      AS public_road_miles,
    TRY_CAST(lanemiles AS BIGINT)      AS lane_miles,
    TRY_CAST(vmt AS BIGINT)            AS vehicle_miles_of_travel_millions
FROM "fhwa-54nx-se7f"
WHERE year IS NOT NULL AND TRY_CAST(year AS INTEGER) IS NOT NULL
