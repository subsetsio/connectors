-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ethnic_nationality",
    "indicator",
    "sex",
    "time_of_immigration_return",
    "citizenship",
    "age_group",
    "place_of_residence",
    "value"
FROM "statistics-estonia-rl0517.px"
