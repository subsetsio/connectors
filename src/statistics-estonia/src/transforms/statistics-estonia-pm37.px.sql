-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "period",
    "indicator",
    "type_of_oleaginous_seeds_and_fruit",
    "value"
FROM "statistics-estonia-pm37.px"
