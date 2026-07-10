-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "state_abbr",
    "state_name",
    "rep_map",
    "rep_map_r_districts",
    "rep_map_d_districts",
    "rep_map_c_districts",
    "rep_map_avg_r_chances",
    "rep_map_avg_d_chances",
    "rep_map_median_pvi",
    "dem_map",
    "dem_map_r_districts",
    "dem_map_d_districts",
    "dem_map_c_districts",
    "dem_map_avg_r_chances",
    "dem_map_avg_d_chances",
    "dem_map_median_pvi",
    "com_map",
    "com_map_r_districts",
    "com_map_d_districts",
    "com_map_c_districts",
    "com_map_avg_r_chances",
    "com_map_avg_d_chances",
    "com_map_median_pvi"
FROM "fivethirtyeight-redistricting-alternate-maps-redistricting-alternate-maps"
