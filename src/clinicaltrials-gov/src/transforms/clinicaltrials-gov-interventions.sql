-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Raw table may repeat identical intervention rows for a study; count distinct nct_id when counting studies by intervention.
SELECT
    "nct_id",
    "intervention_type",
    "intervention_name"
FROM "clinicaltrials-gov-interventions"
