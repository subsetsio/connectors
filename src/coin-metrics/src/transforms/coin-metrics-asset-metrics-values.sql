-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows mix metrics with different definitions and units; filter or group by metric, and use the metric catalog before aggregating values.
SELECT
    "asset",
    "metric",
    "date",
    "value"
FROM "coin-metrics-asset-metrics-values"
