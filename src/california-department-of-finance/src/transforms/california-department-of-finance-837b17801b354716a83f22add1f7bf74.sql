-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "OBJECTID_1" AS objectid_1,
    "OBJECTID" AS objectid,
    "State" AS state,
    "Shape__Are" AS shape_are,
    "Shape__Len" AS shape_len,
    "County" AS county,
    "State_1" AS state_1,
    "StateFIPS" AS statefips,
    "CountyFIPS" AS countyfips,
    "FIPS" AS fips,
    "county2"
FROM "california-department-of-finance-837b17801b354716a83f22add1f7bf74"
