SELECT DISTINCT nct_id, name, agency_class, role
FROM "clinicaltrials-gov-sponsors-collaborators"
WHERE nct_id IS NOT NULL AND name IS NOT NULL
