-- faithful pass-through of Sea Around Us raw catch data.
-- caution: Region families overlap; filter region_type before aggregating across regions.
SELECT
    "region_type",
    "region_id",
    "region_name",
    "year",
    TRY_CAST("entity_id" AS BIGINT) AS "taxon_key",
    "scientific_name",
    "category" AS "taxon",
    "value" AS "landed_value_usd"
FROM "sea-around-us-catch-value-by-taxon"
WHERE "value" IS NOT NULL
  AND "category" IS NOT NULL
