-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "length_of_working_week",
    "total_at_main_place_of_work",
    "ethnic_nationality",
    "age",
    "employment_status",
    "place_of_residence",
    "sex",
    "value"
FROM "statistics-estonia-rl429.px"
