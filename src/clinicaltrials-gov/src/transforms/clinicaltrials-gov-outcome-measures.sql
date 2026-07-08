SELECT nct_id, outcome_type, measure, time_frame
FROM "clinicaltrials-gov-outcome-measures"
WHERE nct_id IS NOT NULL AND measure IS NOT NULL
