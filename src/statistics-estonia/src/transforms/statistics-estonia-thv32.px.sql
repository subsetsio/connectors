-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "disabilty",
    "with_whom_time_was_spent",
    "period",
    "value"
FROM "statistics-estonia-thv32.px"
