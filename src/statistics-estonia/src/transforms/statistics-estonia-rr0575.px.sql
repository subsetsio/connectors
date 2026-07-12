-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "reference_period",
    "type_of_benefit_esa_2010_transaction",
    "indicator",
    "value"
FROM "statistics-estonia-rr0575.px"
