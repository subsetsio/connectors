-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ability_to_speak_a_dialect",
    "sex",
    "place_of_birth",
    "age_group",
    "county",
    "value"
FROM "statistics-estonia-rl0447.px"
