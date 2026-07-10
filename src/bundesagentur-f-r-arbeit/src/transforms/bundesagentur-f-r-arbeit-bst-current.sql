-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is a current-period extract for the Beschaeftigung theme; use the corresponding timeseries table for historical trend analysis.
SELECT
    "metric",
    "period_label",
    "year",
    "month",
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "group_code",
    "group_name",
    "value"
FROM "bundesagentur-f-r-arbeit-bst-current"
