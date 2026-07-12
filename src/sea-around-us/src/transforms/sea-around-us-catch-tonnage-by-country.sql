-- faithful pass-through of Sea Around Us raw catch data.
-- caution: Region families overlap; filter region_type before aggregating across regions.
SELECT
    "region_type",
    "region_id",
    "region_name",
    "year",
    "category" AS "fishing_country",
    "value" AS "catch_tonnes"
FROM "sea-around-us-catch-tonnage-by-country"
WHERE "value" IS NOT NULL
  AND "category" IS NOT NULL
