-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are regional annual estimates; global totals should not be computed by summing all numeric columns without selecting the intended measure.
SELECT
    CAST("year" AS BIGINT) AS year,
    CAST("area_km2" AS DOUBLE) AS area_km2,
    CAST("mwe" AS DOUBLE) AS mwe,
    CAST("mwe_sigma" AS DOUBLE) AS mwe_sigma,
    CAST("gt" AS DOUBLE) AS gt,
    CAST("gt_sigma" AS DOUBLE) AS gt_sigma,
    "region"
FROM "wgms-amce-region"
