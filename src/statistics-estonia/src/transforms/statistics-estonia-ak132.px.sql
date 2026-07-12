-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "day_of_the_week",
    "with_whom_time_is_spent",
    "sex",
    "period",
    "value"
FROM "statistics-estonia-ak132.px"
