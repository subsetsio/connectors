-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ability_to_speak_a_dialect",
    "place_of_residence",
    "age_group",
    "value"
FROM "statistics-estonia-rl0445.px"
