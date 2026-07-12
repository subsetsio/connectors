-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "indicator",
    "type_of_comfort_characteristics",
    "owner",
    "place_of_residence",
    "value"
FROM "statistics-estonia-rl812.px"
