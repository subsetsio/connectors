-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "mobile_penetration_rate"
FROM "sg-data-d-5fb7ffda1ffd756151b1650d4c64363c"
