-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw worksheet contains rows that do not form a scan-verified key before transform filtering; use the observation dimensions and period/date fields together when analyzing the published series.
SELECT
    "series",
    strptime("period", '%Y-%m')::DATE AS period,
    "year",
    "part",
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "value"
FROM "monetary-authority-of-macao-5-external-activities--foreign-assets-jun-84-to-dec-04"
