-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "reservation_date",
    "franchisee_name",
    "status",
    "installation_date",
    "pole_class",
    "borough",
    "x_coord",
    "y_coord",
    "latitude",
    "longitude",
    "_zone" AS zone,
    "on_street",
    "cross_street_1",
    "cross_street_2",
    "park_advisory",
    "historic_landmark_advisory",
    "scenic_landmark_advisory",
    "bid_advisory",
    "school_advisory",
    "zipcode",
    "community_board",
    "council_district"
FROM "nyc-open-data-tbgj-tdd6"
