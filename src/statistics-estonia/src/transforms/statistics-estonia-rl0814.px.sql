-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "time_of_construction",
    "indicator",
    "place_of_residence",
    "type_of_building",
    "value"
FROM "statistics-estonia-rl0814.px"
