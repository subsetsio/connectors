-- faithful pass-through of Sea Around Us raw catch data.
-- caution: Region families overlap; filter region_type before aggregating across regions.
SELECT
    "region_type",
    "region_id",
    "region_name",
    "year",
    "category" AS "reporting_status",
    "value" AS "landed_value_usd"
FROM "sea-around-us-catch-value-by-reporting-status"
WHERE "value" IS NOT NULL
  AND "category" IS NOT NULL
