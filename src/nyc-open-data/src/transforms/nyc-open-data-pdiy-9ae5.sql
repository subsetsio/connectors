-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "cof_id",
    "cof_num",
    "cof_type",
    "holder_name",
    "expires_on",
    "prem_addr",
    "bin",
    "community_board",
    "council_district",
    "bbl",
    "latitude",
    "longitude",
    "postcode",
    "borough",
    "number",
    "street",
    "census_tract",
    "nta"
FROM "nyc-open-data-pdiy-9ae5"
