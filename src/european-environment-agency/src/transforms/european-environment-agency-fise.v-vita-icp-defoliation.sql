SELECT
    CAST("countries" AS VARCHAR) AS "countries",
    CAST("defoliation_type" AS VARCHAR) AS "defoliation_type",
    CAST("tree" AS VARCHAR) AS "tree",
    CAST("units" AS VARCHAR) AS "units",
    CAST("value" AS VARCHAR) AS "value",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.v-vita-icp-defoliation"
