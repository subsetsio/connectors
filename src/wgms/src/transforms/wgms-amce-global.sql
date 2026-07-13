-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Annual and cumulative mass-change measures appear together; do not sum cumulative columns across years.
SELECT
    "year",
    "area_km2",
    "mwe",
    "mwe_sigma",
    "mwe_cumsum",
    "gt",
    "gt_sigma",
    "gt_cumsum",
    "gt_cumsum_sigma",
    "mmsle",
    "mmsle_sigma",
    "mmsle_cumsum",
    "mmsle_cumsum_sigma"
FROM "wgms-amce-global"
