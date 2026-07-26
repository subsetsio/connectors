-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "organization_name",
    "mission",
    "volunteer_program_description",
    "street_address",
    "_2nd_address" AS 2nd_address,
    "city",
    "state",
    "postcode",
    "website",
    "borough",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "census_tract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-i4kb-6ab6"
