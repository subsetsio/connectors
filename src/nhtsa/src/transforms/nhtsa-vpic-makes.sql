SELECT
    TRY_CAST(Make_ID AS BIGINT)          AS make_id,
    NULLIF(TRIM(Make_Name), '')          AS make_name
FROM "nhtsa-vpic-makes"
WHERE Make_ID IS NOT NULL
