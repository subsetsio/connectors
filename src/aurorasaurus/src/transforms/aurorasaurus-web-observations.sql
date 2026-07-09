-- caution: Rows include both positive and negative sighting reports; filter `saw_aurora`
-- before treating rows as observed aurora events.
-- caution: `report_time_start` and `report_time_end` are observer-supplied sighting
-- windows, while `observed_at` is the submission timestamp.
SELECT
    CAST("id" AS BIGINT) AS report_id,
    CAST("timestamp" AS TIMESTAMP) AS observed_at,
    CAST("time_start" AS TIMESTAMP) AS report_time_start,
    TRY_CAST("time_end" AS TIMESTAMP) AS report_time_end,
    TRY_CAST("location".latitude AS DOUBLE) AS latitude,
    TRY_CAST("location".longitude AS DOUBLE) AS longitude,
    "address_country" AS country,
    "address_state" AS state,
    CAST("see_aurora" AS BOOLEAN) AS saw_aurora,
    "sky",
    "sky_other",
    array_to_string("colors", ',') AS colors,
    "colors_other",
    array_to_string("types", ',') AS types,
    "types_other",
    "activities",
    "activities_other",
    "height",
    "height_other",
    CAST("on_going" AS BOOLEAN) AS ongoing,
    CAST("valid" AS BOOLEAN) AS valid,
    "verified",
    "verified_type",
    "comment"
FROM "aurorasaurus-web-observations"
WHERE "id" IS NOT NULL
  AND "time_start" IS NOT NULL
