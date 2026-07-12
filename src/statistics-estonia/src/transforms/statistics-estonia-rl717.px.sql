-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "number_of_rooms",
    "comfort_characteristics",
    "location",
    "value"
FROM "statistics-estonia-rl717.px"
