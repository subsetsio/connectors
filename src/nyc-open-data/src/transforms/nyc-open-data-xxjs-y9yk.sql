-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "boroughdistricts",
    "field_support_liaisondeputy_dir_student_svcs",
    "office_address",
    "office_phone",
    "postcode",
    "borough",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "census_tract",
    "bin",
    "bbl",
    "nta",
    "location_1"
FROM "nyc-open-data-xxjs-y9yk"
