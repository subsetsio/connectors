WITH ranked AS (
    SELECT
        "sighting_id",
        "map_slug",
        CAST("year" AS INTEGER) AS "year",
        "season",
        strptime("date", '%m/%d/%Y')::DATE AS "date",
        make_timestamp(CAST("observed_unix" AS BIGINT) * 1000000) AS "observed_at",
        CAST("latitude" AS DOUBLE) AS "latitude",
        CAST("longitude" AS DOUBLE) AS "longitude",
        CAST("elevation" AS DOUBLE) AS "elevation",
        CAST("interval" AS INTEGER) AS "interval",
        CAST("pin_id" AS INTEGER) AS "pin_id",
        "duration",
        "image_url",
        row_number() OVER (
            PARTITION BY "map_slug", "sighting_id"
            ORDER BY "observed_unix" DESC
        ) AS "rn"
    FROM "journey-north-sightings"
    WHERE "sighting_id" IS NOT NULL
)
SELECT
    "sighting_id",
    "map_slug",
    "year",
    "season",
    "date",
    "observed_at",
    "latitude",
    "longitude",
    "elevation",
    "interval",
    "pin_id",
    "duration",
    "image_url"
FROM ranked
WHERE "rn" = 1
