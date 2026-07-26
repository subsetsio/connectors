-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "bin",
    "boro",
    "feature_carried",
    "feature_crossed",
    "rail_road",
    "bridge_type",
    "other_owner",
    "spans",
    "rating_source",
    "inspection_date",
    "general_recommendation",
    "current_rating",
    "verbal_rating",
    "deck_area_sq_ft",
    "replacement_cost",
    "x_coord_lat",
    "y_coord_lon",
    "cd",
    "cd2",
    "cd3"
FROM "nyc-open-data-4yue-vjfc"
