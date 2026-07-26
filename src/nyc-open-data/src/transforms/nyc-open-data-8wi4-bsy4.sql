-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough",
    "boro",
    "block",
    "lot",
    "bbl",
    "hnum_lo",
    "hnum_hi",
    "str_name",
    "crfn",
    "grantee",
    "deed_date",
    "price",
    "cap_rate",
    "borough_cap_rate",
    "yearqtr",
    "postcode",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "census_tract_2020_from_2023",
    "bin",
    "neighborhood_tabulation_area_nta_2020_from_2023",
    "location1"
FROM "nyc-open-data-8wi4-bsy4"
