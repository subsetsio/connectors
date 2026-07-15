-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "investment_schm_type",
    "no_of_mbrs"
FROM "sg-data-d-29adef1e72b8f9e7f0cbac3d7de0f262"
