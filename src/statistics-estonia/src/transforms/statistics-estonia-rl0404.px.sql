-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "de_facto_marital_status",
    "ethnic_nationality",
    "age",
    "legal_marital_status",
    "sex",
    "place_of_residence",
    "value"
FROM "statistics-estonia-rl0404.px"
