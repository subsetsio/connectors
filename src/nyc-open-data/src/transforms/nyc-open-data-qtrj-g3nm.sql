-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "_month" AS month,
    "total_cash_assistance_recipients",
    "monthly_percent_change",
    "yearly_percent_change"
FROM "nyc-open-data-qtrj-g3nm"
