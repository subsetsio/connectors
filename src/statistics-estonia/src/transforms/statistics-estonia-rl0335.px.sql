-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "duration_of_staying_in_estonia",
    "county",
    "sex",
    "value"
FROM "statistics-estonia-rl0335.px"
