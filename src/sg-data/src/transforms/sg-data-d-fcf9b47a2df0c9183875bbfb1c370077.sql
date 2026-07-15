-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "effective_from",
    "ordinary_wage_ceiling"
FROM "sg-data-d-fcf9b47a2df0c9183875bbfb1c370077"
