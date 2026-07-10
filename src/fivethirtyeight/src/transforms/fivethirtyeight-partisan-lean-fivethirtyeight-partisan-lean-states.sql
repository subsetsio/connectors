-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "state",
    "2022"
FROM "fivethirtyeight-partisan-lean-fivethirtyeight-partisan-lean-states"
