-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "unique_id",
    "publish_date",
    "site_id",
    "status",
    "ppt_id",
    "address",
    "city",
    "state",
    "zip",
    "boro",
    "latitude",
    "longitude",
    "cross_street_1",
    "cross_street_2",
    "corner",
    "install_date",
    "active_date",
    "wifi_status",
    "tablet_status",
    "phone_status",
    "community_board",
    "council_district",
    "census_tract",
    "nta",
    "nta_name"
FROM "nyc-open-data-8s5k-n45n"
