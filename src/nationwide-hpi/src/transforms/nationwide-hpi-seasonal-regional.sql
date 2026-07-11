-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The category column is the published regional breakdown and the measure is seasonally adjusted index; compare categories rather than summing them.
SELECT
    "date",
    "period_label",
    "category",
    "measure",
    "value"
FROM "nationwide-hpi-seasonal-regional"
