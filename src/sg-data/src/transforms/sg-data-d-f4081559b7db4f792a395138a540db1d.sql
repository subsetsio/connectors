-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "types_of_judical_executions",
    "number_of_judical_executions"
FROM "sg-data-d-f4081559b7db4f792a395138a540db1d"
