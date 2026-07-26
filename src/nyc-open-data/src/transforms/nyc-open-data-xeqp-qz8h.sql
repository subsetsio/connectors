-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "collision_id",
    "crash_date",
    "crash_time",
    "crash_police_precinct",
    "crash_borough",
    "total_nonsevere_injuries",
    "total_severe_injuries",
    "total_fatalities",
    "latitude",
    "longitude",
    "on_street",
    "cross_street",
    "address",
    "highway_reference_marker",
    "zipcode",
    "similar_fatalities_severe_injuries_3y_lookback",
    "similar_fatalities_all_injuries_3y_lookback",
    "community_board",
    "council_district",
    "building_identification_number_bin",
    "borough_block_lot_bbl",
    "census_tract_2020",
    "neighborhood_tabulation_area_nta_2020"
FROM "nyc-open-data-xeqp-qz8h"
