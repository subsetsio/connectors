-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "work_pass_type",
    "count"
FROM "sg-data-d-4fb775d3cc311989261fae4ad22dde09"
