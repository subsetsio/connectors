-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "employment_and_socio_economic_status",
    "area_of_dwelling_per_inhabitant",
    "type_of_dwelling",
    "place_of_residence",
    "sex",
    "value"
FROM "statistics-estonia-rl8072.px"
