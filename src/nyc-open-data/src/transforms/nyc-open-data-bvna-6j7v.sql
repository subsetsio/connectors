-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "studio_name",
    "postcode",
    "phone",
    "fax",
    "website",
    "email",
    "location_1",
    "number_and_street_address",
    "borough",
    "latitude",
    "longitude",
    "community_board",
    "community_council",
    "census_tract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-bvna-6j7v"
