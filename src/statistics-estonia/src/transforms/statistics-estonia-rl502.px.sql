-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "age",
    "ethnic_nationality",
    "type_and_composition_of_household_and_person_s_status_in_household",
    "place_of_residence",
    "sex",
    "value"
FROM "statistics-estonia-rl502.px"
