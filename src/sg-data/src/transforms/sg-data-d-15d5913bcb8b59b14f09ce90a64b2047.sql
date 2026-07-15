-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "residential_status",
    "number"
FROM "sg-data-d-15d5913bcb8b59b14f09ce90a64b2047"
