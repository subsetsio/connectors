-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is a current-period extract for Foerderung/berufliche Rehabilitation; use the corresponding timeseries table for historical trend analysis.
-- caution: Rows are split by funding group in group_code/group_name; filter or aggregate those groups deliberately before comparing totals.
SELECT
    "metric",
    "period_label",
    "year",
    "month",
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "group_code",
    "group_name",
    "value"
FROM "bundesagentur-f-r-arbeit-fst-current"
