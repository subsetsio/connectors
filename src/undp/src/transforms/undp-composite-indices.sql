-- caution: iso3/country mix real countries with HDR aggregates (regional groupings,
-- human-development groups, World) under synthetic ZZ* iso3 codes.
-- caution: `indicator` mixes indices with their raw components, so `value` is not on a
-- common scale.
-- rows with no observation (null value) are dropped.
SELECT
    "iso3",
    "country",
    "hdicode",
    "region",
    "indicator",
    CAST("year" AS INTEGER) AS year,
    CAST("value" AS DOUBLE) AS value
FROM "undp-composite-indices"
WHERE "value" IS NOT NULL
