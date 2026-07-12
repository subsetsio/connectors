-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "area_of_dwelling",
    "location",
    "type_of_building",
    "value"
FROM "statistics-estonia-rl722.px"
