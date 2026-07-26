-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date_received",
    "borough",
    "community_board",
    "on_street",
    "cross_street_1",
    "cross_street_2",
    "address",
    "block",
    "lot",
    "existing_bus_pad_or_no_bus_pad",
    "if_existing_length_of_bus_pad_feet",
    "bus_padroadway_condition_rating_high_medium_low",
    "vehicular_traffic_high_medium_low",
    "pedestrian_traffic_high_medium_low",
    "curb_type",
    "curb_reveal_inches",
    "sidewalk_type",
    "landmark_area_yesno",
    "ta_structure_yesno",
    "vault_yesno",
    "repaired_yn",
    "contract",
    "construction_date",
    "linear_ft_constructed",
    "postcode",
    "latitude",
    "longitude",
    "council_district",
    "census_tract_2020",
    "bin",
    "bbl",
    "nta_2020"
FROM "nyc-open-data-eyb2-p5s8"
