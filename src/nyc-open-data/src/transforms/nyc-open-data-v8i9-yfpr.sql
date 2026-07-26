-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "permit_number",
    "expiration_date",
    "status",
    "business_name",
    "address_no",
    "address_st",
    "borough",
    "city",
    "state",
    "zipcode",
    "bbl",
    "bin",
    "census_tract_2010",
    "city_council_district",
    "community_district",
    "nta_code",
    "latitude",
    "longitude"
FROM "nyc-open-data-v8i9-yfpr"
