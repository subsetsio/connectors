-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "reference_period",
    "agricultural_unit",
    "county",
    "agricultural_product",
    "indicator",
    "value"
FROM "statistics-estonia-pm09.px"
