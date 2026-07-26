-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "generated_on",
    "site_id",
    "status",
    "planned_kiosk_type",
    "ppt_id",
    "address",
    "city",
    "state",
    "postcode",
    "borough",
    "latitude",
    "longitude",
    "cross_street_1",
    "cross_street_2",
    "corner_location",
    "community_board",
    "council_district",
    "census_tract",
    "nta",
    "bbl",
    "bin",
    "installation_date",
    "activation_date",
    "wifi_status",
    "wifi_last_ts",
    "tablet_status",
    "tablet_last_ts",
    "phone_status",
    "dialer_last_ts",
    "_location" AS location
FROM "nyc-open-data-n6c5-95xh"
