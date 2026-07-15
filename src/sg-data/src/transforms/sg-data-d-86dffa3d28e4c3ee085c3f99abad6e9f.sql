-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "occupation",
    "job_vacancy"
FROM "sg-data-d-86dffa3d28e4c3ee085c3f99abad6e9f"
