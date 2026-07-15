-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "period",
    "category",
    "type",
    "cumulative_number"
FROM "sg-data-d-f8408eaf8ecf45adae760a035b8d850d"
