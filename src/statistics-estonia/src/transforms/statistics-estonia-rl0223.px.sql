-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "main_heating_option",
    "occupancy",
    "type_of_building",
    "location",
    "value"
FROM "statistics-estonia-rl0223.px"
