-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "industry",
    "occupation",
    "resignation_rate"
FROM "sg-data-d-30dfba375648a2d5a1c1099cb9cb8182"
