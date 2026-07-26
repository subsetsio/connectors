-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "permit_number",
    "expiration_date",
    "address_no",
    "address_st",
    "bo",
    "zip",
    "bbl",
    "bin",
    "census_tract_2010",
    "city_council_district",
    "community_district",
    "nta_code",
    "latitude",
    "longitude"
FROM "nyc-open-data-gnyq-kf2y"
