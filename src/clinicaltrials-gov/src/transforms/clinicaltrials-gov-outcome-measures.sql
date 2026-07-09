-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Long table of primary and secondary outcome rows; a single study can have multiple measures of each outcome_type.
SELECT
    "nct_id",
    "outcome_type",
    "measure",
    "time_frame"
FROM "clinicaltrials-gov-outcome-measures"
