-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "age_of_woman",
    "age_of_man",
    "marital_status",
    "place_of_residence",
    "value"
FROM "statistics-estonia-rl206.px"
