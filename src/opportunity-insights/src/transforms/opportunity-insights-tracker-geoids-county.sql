-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "countyfips",
    "countyname",
    "cityid",
    "cityname",
    "cz",
    "czname",
    "statename",
    "statefips",
    "stateabbrev",
    "county_pop2019"
FROM "opportunity-insights-tracker-geoids-county"
