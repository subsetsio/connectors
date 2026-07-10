SELECT
    CAST("broadleaved" AS VARCHAR) AS "broadleaved",
    CAST("coniferous" AS VARCHAR) AS "coniferous",
    CAST("country" AS VARCHAR) AS "country",
    CAST("forest" AS VARCHAR) AS "forest",
    CAST("other_wooded_land" AS VARCHAR) AS "other_wooded_land",
    CAST("total_forest_and_other_wooded_land" AS VARCHAR) AS "total_forest_and_other_wooded_land",
    CAST("variable" AS VARCHAR) AS "variable",
    CAST("year" AS VARCHAR) AS "year"
FROM "european-environment-agency-fise.foresteurope-deadwood"
