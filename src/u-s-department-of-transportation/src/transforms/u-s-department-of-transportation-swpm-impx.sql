-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("month" AS TIMESTAMP) AS month,
    CAST("reliability_rate" AS DOUBLE) AS reliability_rate,
    CAST("tonnage_metric_tons" AS BIGINT) AS tonnage_metric_tons,
    CAST("tonnage_short_tons" AS DOUBLE) AS tonnage_short_tons,
    CAST("vessel_transits" AS BIGINT) AS vessel_transits,
    "note"
FROM "u-s-department-of-transportation-swpm-impx"
