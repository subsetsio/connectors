-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "time_of_last_migration",
    "sex",
    "previous_place_of_residence",
    "county",
    "age_group",
    "ethnic_nationality",
    "value"
FROM "statistics-estonia-rl0545.px"
