SELECT
    state,
    TRY_CAST(hpms_toll_id AS INTEGER) AS hpms_toll_id,
    name_of_toll_facility
FROM "fhwa-8fiq-4cn6"
WHERE state IS NOT NULL AND hpms_toll_id IS NOT NULL
