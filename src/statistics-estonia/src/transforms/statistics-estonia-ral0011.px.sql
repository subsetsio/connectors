-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "reference_period",
    "adjustment",
    "employed_persons",
    "economic_activity",
    "indicator",
    "value"
FROM "statistics-estonia-ral0011.px"
