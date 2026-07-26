-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "recordid",
    "address",
    "house_number",
    "street",
    "postcode_original",
    "community_board_original",
    "site",
    "species",
    "diameter",
    "condition",
    "wires",
    "sidewalk_condition",
    "support_structure",
    "borough",
    "x",
    "y",
    "longitude",
    "latitude",
    "cb_new",
    "zip_new",
    "censustract_2010",
    "censusblock_2010",
    "nta_2010",
    "segmentid",
    "spc_common",
    "spc_latin",
    "_location" AS location,
    "council_district",
    "bin",
    "bbl"
FROM "nyc-open-data-kyad-zm4j"
