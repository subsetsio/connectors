-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "limits_granted",
    "utilised",
    "non-performing_percentage" AS non_performing_percentage
FROM "sg-data-d-2d2ca1bcac71713d2c02deca871ebe98"
