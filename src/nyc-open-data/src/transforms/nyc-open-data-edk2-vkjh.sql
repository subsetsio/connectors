-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough",
    "ntaname",
    "site_type",
    "site_name",
    "zipcode",
    "phone_number",
    "days_hours",
    "siteaddr",
    "borocd",
    "notes",
    "dsny_zone",
    "dsny_district",
    "dsny_section",
    "census_tract",
    "community_district",
    "council_district",
    "senate_district",
    "congress_district",
    "assembly_district",
    "police_precinct",
    "bbl",
    "bin",
    "latitude",
    "longitude",
    "point"
FROM "nyc-open-data-edk2-vkjh"
