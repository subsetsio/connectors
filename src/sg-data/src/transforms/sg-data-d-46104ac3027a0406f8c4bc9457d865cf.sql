-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "allocation_mode",
    "gross_allocation"
FROM "sg-data-d-46104ac3027a0406f8c4bc9457d865cf"
