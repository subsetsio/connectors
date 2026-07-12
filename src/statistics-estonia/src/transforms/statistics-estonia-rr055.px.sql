-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sector",
    "revenue_and_expenditure",
    "type_of_revenue_expenditure",
    "indicator",
    CAST("reference_period" AS BIGINT) AS reference_period,
    "value"
FROM "statistics-estonia-rr055.px"
