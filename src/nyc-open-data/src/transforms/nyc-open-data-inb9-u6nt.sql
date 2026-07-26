-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_type" AS type,
    "status",
    "created_date",
    "delivered",
    "delivery_date",
    "received",
    "receive_date",
    "withdrawn",
    "withdraw_date",
    "expired",
    "expire_date",
    "locker_name",
    "locker_box_door",
    "pickup_duration",
    "delivery_duration",
    "collect_duration",
    "send_duration",
    "location_type",
    "address",
    "latitude",
    "longitude",
    "borough",
    "community_board",
    "council_district",
    "bin",
    "bbl",
    "census_tract_2020",
    "neighborhood_tabulation_area_nta_2020"
FROM "nyc-open-data-inb9-u6nt"
