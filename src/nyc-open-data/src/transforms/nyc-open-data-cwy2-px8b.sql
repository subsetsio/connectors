-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "unique_key",
    "created_date",
    "closed_date",
    "agency",
    "agency_name",
    "complaint_type",
    "descriptor",
    "additional_details",
    "location_type",
    "incident_zip",
    "incident_address",
    "street_name",
    "cross_street_1",
    "cross_street_2",
    "intersection_street_1",
    "intersection_street_2",
    "address_type",
    "city",
    "landmark",
    "status",
    "due_date",
    "resolution_description",
    "resolution_action_updated_date",
    "community_board",
    "council_district",
    "bbl",
    "borough",
    "x_coordinate_state_plane",
    "y_coordinate_state_plane",
    "open_data_channel_type",
    "latitude",
    "longitude",
    "_location" AS location
FROM "nyc-open-data-cwy2-px8b"
