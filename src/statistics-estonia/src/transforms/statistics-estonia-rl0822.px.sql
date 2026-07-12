-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "area_of_dwelling",
    "type_of_building",
    "number_of_rooms",
    "place_of_residence",
    "indicator",
    "value"
FROM "statistics-estonia-rl0822.px"
