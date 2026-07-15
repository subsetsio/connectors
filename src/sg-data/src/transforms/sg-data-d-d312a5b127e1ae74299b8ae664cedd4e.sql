-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "stn_code",
    "mrt_station_english",
    "mrt_station_chinese",
    "mrt_line_english",
    "mrt_line_chinese"
FROM "sg-data-d-d312a5b127e1ae74299b8ae664cedd4e"
