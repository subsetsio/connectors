SELECT DISTINCT nct_id, intervention_type, intervention_name
FROM "clinicaltrials-gov-interventions"
WHERE nct_id IS NOT NULL AND intervention_name IS NOT NULL
