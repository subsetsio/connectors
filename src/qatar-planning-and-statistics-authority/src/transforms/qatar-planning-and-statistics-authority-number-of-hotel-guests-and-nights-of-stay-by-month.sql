-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "month_ar",
    "year",
    "sn",
    "value"
FROM "qatar-planning-and-statistics-authority-number-of-hotel-guests-and-nights-of-stay-by-month"
