-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "number_of_children_given_birth_to",
    "de_facto_marital_status",
    "ethnic_nationality_of_woman",
    "age_of_woman",
    "legal_marital_status",
    "place_of_residence",
    "value"
FROM "statistics-estonia-rl211.px"
