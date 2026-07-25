-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows combine modeled tide, surge, and percentile water-level fields for harbor feeds; observed_at is the water-level timestamp while updated identifies the source feed update.
SELECT
    "harbor",
    "updated",
    "observed_at",
    "surge",
    "tide",
    "total",
    "p0",
    "p25",
    "p50",
    "p75",
    "p100",
    "fetched_at"
FROM "norwegian-meteorological-institute-tidalwater"
