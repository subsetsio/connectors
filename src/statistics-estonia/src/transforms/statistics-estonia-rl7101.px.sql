-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "owner",
    "occupancy",
    "type_of_dwelling",
    "location",
    "value"
FROM "statistics-estonia-rl7101.px"
