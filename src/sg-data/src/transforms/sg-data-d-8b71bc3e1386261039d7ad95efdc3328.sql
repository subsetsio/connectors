-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "ec_completion_status",
    "sale_status",
    "units"
FROM "sg-data-d-8b71bc3e1386261039d7ad95efdc3328"
