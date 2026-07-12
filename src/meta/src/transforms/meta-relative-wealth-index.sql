-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Some source files do not provide quadkeys, so the row identity is the source file plus coordinate and measured values.
-- caution: Relative Wealth Index values are comparable as modeled estimates, not counts or totals.
SELECT
    "quadkey",
    "latitude",
    "longitude",
    "rwi",
    "error",
    "_source_file" AS source_file
FROM "meta-relative-wealth-index"
