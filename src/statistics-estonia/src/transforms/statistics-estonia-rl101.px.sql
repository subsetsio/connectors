-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sex",
    "de_facto_and_usual_resident_population",
    "administrative_unit",
    "value"
FROM "statistics-estonia-rl101.px"
