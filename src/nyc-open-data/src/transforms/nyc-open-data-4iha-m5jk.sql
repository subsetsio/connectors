-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "communityboard",
    "gispropnum",
    "multipolygon",
    "park_area_desc",
    "park_area_id",
    "park_area_loc",
    "park_borough",
    "park_district",
    "police_boro_com",
    "police_precinct",
    "reported_as"
FROM "nyc-open-data-4iha-m5jk"
