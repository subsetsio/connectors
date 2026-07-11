-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "area",
    "iso",
    "sex",
    "year",
    "age",
    "metric",
    "value"
FROM "ncd-risc-ncd-risc-nature-2020-cholesterol-age-standardised-countries"
