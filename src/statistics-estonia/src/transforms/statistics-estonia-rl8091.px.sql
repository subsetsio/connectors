-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "area_of_dwelling_per_inhabitant",
    "type_of_dwelling",
    "occupancy_and_composition_of_households",
    "place_of_residence",
    "value"
FROM "statistics-estonia-rl8091.px"
