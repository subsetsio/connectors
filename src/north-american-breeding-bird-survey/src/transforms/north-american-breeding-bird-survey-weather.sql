-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Weather and effort fields describe the survey run conditions and are not bird-count observations.
SELECT
    CAST("RouteDataID" AS BIGINT) AS routedataid,
    CAST("CountryNum" AS BIGINT) AS countrynum,
    "StateNum" AS statenum,
    "Route" AS route,
    CAST("RPID" AS BIGINT) AS rpid,
    CAST("Year" AS BIGINT) AS year,
    "Month" AS month,
    "Day" AS day,
    "ObsN" AS obsn,
    "TotalSpp" AS totalspp,
    "StartTemp" AS starttemp,
    "EndTemp" AS endtemp,
    "TempScale" AS tempscale,
    CAST("StartWind" AS BIGINT) AS startwind,
    CAST("EndWind" AS BIGINT) AS endwind,
    CAST("StartSky" AS BIGINT) AS startsky,
    CAST("EndSky" AS BIGINT) AS endsky,
    "StartTime" AS starttime,
    "EndTime" AS endtime,
    "Assistant" AS assistant,
    CAST("QualityCurrentID" AS BIGINT) AS qualitycurrentid,
    CAST("RunType" AS BIGINT) AS runtype
FROM "north-american-breeding-bird-survey-weather"
