SELECT region,
       country
FROM "global-carbon-project-national-fossil-regions"
WHERE region IS NOT NULL
  AND country IS NOT NULL
