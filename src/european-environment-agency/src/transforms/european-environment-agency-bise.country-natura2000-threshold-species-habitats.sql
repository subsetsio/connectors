SELECT
    CAST("country_code" AS VARCHAR) AS "country_code",
    CAST("more_than_10_features" AS VARCHAR) AS "more_than_10_features",
    CAST("more_than_20_features" AS VARCHAR) AS "more_than_20_features",
    CAST("one_feature" AS VARCHAR) AS "one_feature"
FROM "european-environment-agency-bise.country-natura2000-threshold-species-habitats"
