-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "period_start",
    "period_end",
    "income_quintile",
    "percentage_expenditure_on_healthcare"
FROM "sg-data-d-59f95bfb94f977cc3d9e74ac6f156ab5"
