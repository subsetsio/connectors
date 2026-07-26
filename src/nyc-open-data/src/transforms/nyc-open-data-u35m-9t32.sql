-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "organization_name",
    "address",
    "city",
    "state",
    "postcode",
    "main_phone",
    "discipline",
    "council_district",
    "community_board",
    "borough",
    "latitude",
    "longitude",
    "census_tract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-u35m-9t32"
