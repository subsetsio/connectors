SELECT DISTINCT
    nct_id, facility, city, state, zip, country, location_status
FROM "clinicaltrials-gov-locations"
WHERE nct_id IS NOT NULL
