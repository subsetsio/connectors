-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "effective_from",
    "full_retirement_sum"
FROM "sg-data-d-b212dff55c98a4c0b3d3d850bf744ad7"
