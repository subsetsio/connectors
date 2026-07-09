-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Borrower income levels are stored as separate year-over-year measure columns, so do not sum those columns together.
SELECT
    "month",
    strptime("date", '%Y-%m')::DATE AS date,
    "low_yoy",
    "moderate_yoy",
    "middle_yoy",
    "high_yoy",
    "market"
FROM "cfpb-cct-yoy-data-income-level"
