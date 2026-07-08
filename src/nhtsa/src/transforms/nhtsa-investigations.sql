SELECT
    NULLIF(TRIM(NHTSA_ACTION_NUMBER), '')                     AS action_number,
    NULLIF(TRIM(MAKE), '')                                    AS make,
    NULLIF(TRIM(MODEL), '')                                   AS model,
    TRY_CAST(NULLIF(YEAR, '9999') AS INTEGER)               AS model_year,
    NULLIF(TRIM(COMPNAME), '')                               AS component,
    NULLIF(TRIM(MFR_NAME), '')                               AS manufacturer,
    TRY_CAST(strptime(NULLIF(ODATE, ''), '%Y%m%d') AS DATE) AS open_date,
    TRY_CAST(strptime(NULLIF(CDATE, ''), '%Y%m%d') AS DATE) AS close_date,
    NULLIF(TRIM(CAMPNO), '')                                 AS related_campaign,
    NULLIF(SUBJECT, '')                                      AS subject,
    NULLIF(SUMMARY, '')                                      AS summary
FROM "nhtsa-investigations"
WHERE NHTSA_ACTION_NUMBER IS NOT NULL AND TRIM(NHTSA_ACTION_NUMBER) <> ''
