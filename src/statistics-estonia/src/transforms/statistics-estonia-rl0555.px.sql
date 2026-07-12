-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "county_2000",
    "age_group",
    "county",
    "sex",
    "ethnic_nationality",
    "value"
FROM "statistics-estonia-rl0555.px"
