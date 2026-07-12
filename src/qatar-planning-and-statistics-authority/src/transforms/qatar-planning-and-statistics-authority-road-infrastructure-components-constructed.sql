-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "month",
    "pavement_length_linear_km",
    "number_of_street_lighting_poles",
    "number_of_traffic_sign",
    "number_of_traffic_signal",
    "number_of_stuctures",
    "number_of_speed_hump",
    "number_of_its",
    "road_marking_length_km",
    "number_of_street_sign"
FROM "qatar-planning-and-statistics-authority-road-infrastructure-components-constructed"
