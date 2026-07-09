-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Year-over-year measures are percentages or index changes, not additive counts.
SELECT
    "month",
    strptime("date", '%Y-%m')::DATE AS date,
    "yoy_num",
    "yoy_vol",
    "market"
FROM "cfpb-cct-yoy-data-all"
