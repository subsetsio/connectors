-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Coefficient" AS coefficient,
    "Linkage_Forward" AS linkage_forward,
    "Linkage_Backward" AS linkage_backward
FROM "sg-data-d-7ceb02cbfc31b35d8308ea51e6a38c9d"
