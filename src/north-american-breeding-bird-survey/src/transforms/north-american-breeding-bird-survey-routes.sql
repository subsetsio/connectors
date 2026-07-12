-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Routes are reference geography, not annual survey runs; join to count and weather tables using country, state, and route identifiers.
SELECT
    CAST("CountryNum" AS BIGINT) AS countrynum,
    "StateNum" AS statenum,
    "Route" AS route,
    "RouteName" AS routename,
    "Active" AS active,
    "Latitude" AS latitude,
    "Longitude" AS longitude,
    "Stratum" AS stratum,
    "BCR" AS bcr,
    CAST("RouteTypeID" AS BIGINT) AS routetypeid,
    CAST("RouteTypeDetailID" AS BIGINT) AS routetypedetailid
FROM "north-american-breeding-bird-survey-routes"
