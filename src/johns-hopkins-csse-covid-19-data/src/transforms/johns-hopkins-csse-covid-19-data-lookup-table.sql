-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The lookup table mixes global country/province rows with US county rows; join on the identifier that matches the target table's geography level.
SELECT
    CAST("uid" AS BIGINT) AS uid,
    "iso2",
    "iso3",
    CAST("code3" AS BIGINT) AS code3,
    "fips",
    "admin2",
    "province_state",
    "country_region",
    CAST("lat" AS DOUBLE) AS lat,
    CAST("long" AS DOUBLE) AS long,
    "combined_key",
    CAST("population" AS BIGINT) AS population
FROM "johns-hopkins-csse-covid-19-data-lookup-table"
