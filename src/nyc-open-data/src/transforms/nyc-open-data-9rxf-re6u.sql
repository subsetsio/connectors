-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "neighborhood_tabulation_area_code_nta_code",
    "neighborhood_tabulation_area_name_nta_name",
    "borough_name",
    "published_date",
    "neighborhood_tabulation_area_nta_total_area",
    "pedestrian_corridor_area_in_square_miles",
    "number_of_wifi_hotspots_in_nta",
    "access_points_in_pedestrian_corridor",
    "access_points_per_square_mile_of_pedestrian_corridors",
    "public_computer_centers_with_wifi"
FROM "nyc-open-data-9rxf-re6u"
