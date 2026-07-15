-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "industry1",
    "sick_leave",
    "proportion"
FROM "sg-data-d-6fc4532c1cf7d5a1a231c89f4c835530"
