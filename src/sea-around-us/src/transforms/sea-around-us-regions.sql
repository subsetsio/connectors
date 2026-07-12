SELECT
    "region_type",
    "region_id",
    "title",
    "long_title"
FROM "sea-around-us-regions"
WHERE "region_type" IS NOT NULL
  AND "region_id" IS NOT NULL
