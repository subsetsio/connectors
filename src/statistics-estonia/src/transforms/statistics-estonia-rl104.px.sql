-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "permanent_place_of_residence",
    "location_at_the_moment_of_census",
    "sex",
    "value"
FROM "statistics-estonia-rl104.px"
