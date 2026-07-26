-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "facilityname",
    "service_category",
    "service_type",
    "address",
    "address_2",
    "borough",
    "postcode",
    "latitude",
    "longitude",
    "phone_number",
    "additionalinfo",
    "intake",
    "paymentcost",
    "special_populations_served",
    "monday",
    "tuesday",
    "wednsday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
    "website",
    "community_board",
    "city_council",
    "bin",
    "bbl",
    "census_tract",
    "nta"
FROM "nyc-open-data-nk7g-qeep"
