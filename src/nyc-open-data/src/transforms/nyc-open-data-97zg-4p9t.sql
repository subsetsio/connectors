-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "fy",
    "_type" AS type,
    "received",
    "address",
    "bor_name",
    "block",
    "lot",
    "bbl",
    "landm_type",
    "app_status",
    "staff_action",
    "board_action",
    "amount",
    "prj_status",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "census_tract",
    "bin",
    "nta",
    "postcode"
FROM "nyc-open-data-97zg-4p9t"
