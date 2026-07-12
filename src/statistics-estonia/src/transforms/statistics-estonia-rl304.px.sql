-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "general_education",
    "vocational_or_professional_education",
    "ethnic_nationality",
    "place_of_residence",
    "sex",
    "value"
FROM "statistics-estonia-rl304.px"
