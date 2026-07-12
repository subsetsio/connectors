-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "socio_economic_status_length_of_working_week",
    "ethnic_nationality",
    "importance_of_source_of_subsistence",
    "source_of_subsistence",
    "place_of_residence",
    "sex",
    "value"
FROM "statistics-estonia-rl404.px"
