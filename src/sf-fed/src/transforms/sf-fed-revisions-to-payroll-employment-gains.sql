-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sheet",
    "row_idx",
    "period",
    "period_date",
    "series",
    "value",
    strptime("value_text", '%Y-%m-%d')::DATE AS value_text
FROM "sf-fed-revisions-to-payroll-employment-gains"
