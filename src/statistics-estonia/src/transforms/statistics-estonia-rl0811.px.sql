-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "age_group",
    "sex",
    "number_of_inhabitants_in_dwelling",
    "number_of_rooms",
    "county",
    "value"
FROM "statistics-estonia-rl0811.px"
