SELECT DISTINCT nct_id, condition
FROM "clinicaltrials-gov-conditions"
WHERE nct_id IS NOT NULL AND condition IS NOT NULL
