-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "area_of_dwelling_per_inhabitant",
    "sex",
    "age_group",
    "county",
    "ethnic_nationality",
    "value"
FROM "statistics-estonia-rl0809.px"
