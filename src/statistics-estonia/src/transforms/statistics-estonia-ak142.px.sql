-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "age_group",
    "with_whom_time_is_spent",
    "sex",
    "period",
    "value"
FROM "statistics-estonia-ak142.px"
