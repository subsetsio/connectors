-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Long table of study-condition associations; count distinct nct_id when counting studies by condition.
SELECT
    "nct_id",
    "condition"
FROM "clinicaltrials-gov-conditions"
