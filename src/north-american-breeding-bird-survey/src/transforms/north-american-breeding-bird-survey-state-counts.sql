-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table is wide by five 10-stop count bins plus a route total; unpivot count bins before treating them as repeated stop-group observations.
SELECT
    CAST("RouteDataID" AS BIGINT) AS routedataid,
    CAST("CountryNum" AS BIGINT) AS countrynum,
    "StateNum" AS statenum,
    "Route" AS route,
    CAST("RPID" AS BIGINT) AS rpid,
    CAST("Year" AS BIGINT) AS year,
    "AOU" AS aou,
    "Count10" AS count10,
    "Count20" AS count20,
    "Count30" AS count30,
    "Count40" AS count40,
    "Count50" AS count50,
    "StopTotal" AS stoptotal,
    "SpeciesTotal" AS speciestotal
FROM "north-american-breeding-bird-survey-state-counts"
