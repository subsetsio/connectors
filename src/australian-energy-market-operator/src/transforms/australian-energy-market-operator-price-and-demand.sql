-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The settlement interval cadence changes historically: older observations are 30-minute intervals and recent observations are 5-minute intervals, so interval counts should not be compared across eras without accounting for cadence.
-- caution: The region domain includes historical SNOWY1 alongside current NEM regions; filter or group regions deliberately when calculating current-market totals.
SELECT
    "region",
    "settlement_date",
    "total_demand",
    "rrp",
    "period_type"
FROM "australian-energy-market-operator-price-and-demand"
