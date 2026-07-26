-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "oft_code",
    "project_type",
    "borough_code",
    "location_on_street",
    "location_from_street",
    "location_to_street",
    "project_id",
    "project_status",
    "project_speed_bumps",
    "location_community_board",
    strptime("location_actual_milling_start_date", '%m/%d/%Y')::DATE AS location_actual_milling_start_date,
    strptime("location_actual_milling_end_date", '%m/%d/%Y')::DATE AS location_actual_milling_end_date,
    strptime("location_actual_paving_start_date", '%m/%d/%Y')::DATE AS location_actual_paving_start_date,
    strptime("location_actual_paving_end_date", '%m/%d/%Y')::DATE AS location_actual_paving_end_date,
    strptime("location_actual_protect_until", '%m/%d/%Y')::DATE AS location_actual_protect_until,
    "location_actual_lane_miles_paved",
    "location_actual_paving_square_yard",
    "location_status",
    "location_segment_id",
    "location_wkt",
    CAST("location_node_id" AS BIGINT) AS location_node_id
FROM "nyc-open-data-ffaf-8mrv"
