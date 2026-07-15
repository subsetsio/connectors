-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "total_loans",
    "total_loans_business",
    "total_loans_consumer"
FROM "sg-data-d-0239d0d67315994c63a04e6f7bdc08cc"
