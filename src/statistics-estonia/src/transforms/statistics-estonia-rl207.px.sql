-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ethnic_nationality_of_woman",
    "ethnic_nationality_of_man",
    "marital_status",
    "place_of_residence",
    "value"
FROM "statistics-estonia-rl207.px"
