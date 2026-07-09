SELECT
    metro,
    county,
    state
FROM "american-enterprise-institute-metro-counties"
WHERE metro IS NOT NULL
  AND county IS NOT NULL
  AND state IS NOT NULL
