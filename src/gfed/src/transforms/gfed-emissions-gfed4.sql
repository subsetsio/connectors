-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Includes GFED aggregate categories such as global region and total fire type; filter aggregation rows before summing across regions or fire types.
-- caution: GFED4.1s years from 2017 onward are beta/extrapolated values and should not be treated as trend-comparable with the finalized historical period without consulting source guidance.
SELECT
    "species",
    "fire_type",
    "region",
    "year",
    "value",
    "unit"
FROM "gfed-emissions-gfed4"
