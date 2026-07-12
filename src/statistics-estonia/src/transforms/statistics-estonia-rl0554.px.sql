-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "county",
    "place_of_residence_2000",
    "age_group",
    "sex",
    "value"
FROM "statistics-estonia-rl0554.px"
