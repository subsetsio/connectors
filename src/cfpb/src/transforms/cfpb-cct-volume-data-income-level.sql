-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are segmented by borrower income group and market; totals across income groups may duplicate all-market views published in other tables.
SELECT
    "month",
    strptime("date", '%Y-%m')::DATE AS date,
    "vol",
    "vol_unadj",
    "income_level_group",
    "market"
FROM "cfpb-cct-volume-data-income-level"
