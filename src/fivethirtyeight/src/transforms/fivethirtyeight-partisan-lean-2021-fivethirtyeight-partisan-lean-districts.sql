-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "district",
    "2021"
FROM "fivethirtyeight-partisan-lean-2021-fivethirtyeight-partisan-lean-districts"
