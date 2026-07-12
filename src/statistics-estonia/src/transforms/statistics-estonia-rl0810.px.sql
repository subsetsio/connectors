-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "employment_and_socio_economic_status",
    "sex",
    "area_of_dwelling_per_inhabitant",
    "type_of_building",
    "age_group",
    "county",
    "value"
FROM "statistics-estonia-rl0810.px"
