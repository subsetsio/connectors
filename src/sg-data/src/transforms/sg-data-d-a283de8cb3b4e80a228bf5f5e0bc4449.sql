-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "res_completion_status",
    "units"
FROM "sg-data-d-a283de8cb3b4e80a228bf5f5e0bc4449"
