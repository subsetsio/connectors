-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "time_of_construction",
    "type_of_building_and_number_of_dwellings_in_the_building",
    "county",
    "value"
FROM "statistics-estonia-rl0212.px"
