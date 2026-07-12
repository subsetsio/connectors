-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "reference_period",
    "sex",
    "group_of_persons",
    "indicator",
    "value"
FROM "statistics-estonia-tt3320.px"
