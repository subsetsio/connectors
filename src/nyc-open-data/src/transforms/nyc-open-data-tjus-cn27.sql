-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "parid",
    "borocode",
    "block",
    "lot",
    "taxyear",
    "street_number",
    "street_name",
    "postcode",
    "bldg_class",
    "taxclass",
    "owner_name",
    "borough",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "census_tract",
    "bin",
    "bbl",
    "nta_name",
    "nta_code2"
FROM "nyc-open-data-tjus-cn27"
