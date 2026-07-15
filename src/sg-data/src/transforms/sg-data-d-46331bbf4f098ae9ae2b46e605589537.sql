-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "competency_types",
    "no_of_active_licenses"
FROM "sg-data-d-46331bbf4f098ae9ae2b46e605589537"
