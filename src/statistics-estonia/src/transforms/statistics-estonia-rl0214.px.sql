-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "time_of_construction",
    "area_of_dwelling",
    "type_of_building",
    "county",
    "value"
FROM "statistics-estonia-rl0214.px"
