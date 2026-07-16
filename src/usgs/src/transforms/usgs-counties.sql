-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "country_code",
    "state_fips_code",
    "county_fips_code",
    "county_name",
    "_lon" AS lon,
    "_lat" AS lat
FROM "usgs-counties"
