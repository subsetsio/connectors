-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "monitoring_location_id",
    "field_visit_id",
    "measurement_number",
    CAST("time" AS TIMESTAMP) AS time,
    "channel_name",
    CAST("channel_flow" AS DOUBLE) AS channel_flow,
    "channel_flow_unit",
    "channel_width",
    "channel_width_unit",
    "channel_area",
    "channel_area_unit",
    "channel_velocity",
    "channel_velocity_unit",
    "channel_location_distance",
    "channel_location_distance_unit",
    "channel_stability",
    "channel_material",
    "channel_evenness",
    "horizontal_velocity_description",
    "vertical_velocity_description",
    "longitudinal_velocity_description",
    "measurement_type",
    "last_modified",
    "channel_measurement_type",
    "channel_location_direction",
    CAST("_lon" AS DOUBLE) AS lon,
    CAST("_lat" AS DOUBLE) AS lat
FROM "usgs-channel-measurements"
