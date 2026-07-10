SELECT
    CAST("area1" AS VARCHAR) AS "area1",
    CAST("area2" AS VARCHAR) AS "area2",
    CAST("DATASET" AS VARCHAR) AS "DATASET",
    CAST("diff" AS VARCHAR) AS "diff",
    CAST("diff_pct" AS VARCHAR) AS "diff_pct",
    CAST("FID" AS VARCHAR) AS "FID",
    CAST("geometry" AS VARCHAR) AS "geometry",
    CAST("LEVL_CODE" AS VARCHAR) AS "LEVL_CODE",
    CAST("NUTS_ID" AS VARCHAR) AS "NUTS_ID",
    CAST("NUTS_NAME" AS VARCHAR) AS "NUTS_NAME",
    CAST("NUTS0" AS VARCHAR) AS "NUTS0",
    CAST("NUTS0_NAME" AS VARCHAR) AS "NUTS0_NAME",
    CAST("resolution" AS VARCHAR) AS "resolution",
    CAST("YEAR1" AS VARCHAR) AS "YEAR1",
    CAST("YEAR2" AS VARCHAR) AS "YEAR2"
FROM "european-environment-agency-fise.ms-comparison-hr"
