-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "datasourceid",
    "startofperiod",
    "endofperiod",
    "locationlatitude",
    "locationlongitude",
    "pm2_5concmass1hourmeanvalue",
    "pm2_5concmassnowcastusepaaqivalue",
    "latitudelongitude"
FROM "nyc-open-data-2juy-aj8e"
