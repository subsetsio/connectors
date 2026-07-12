-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "reference_period",
    "revenue_and_expenditure",
    "type_of_revenue_expenditure",
    "indicator",
    "value"
FROM "statistics-estonia-rr057.px"
