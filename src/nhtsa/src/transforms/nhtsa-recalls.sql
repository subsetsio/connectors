SELECT
    TRY_CAST(RECORD_ID AS BIGINT)                              AS record_id,
    NULLIF(TRIM(CAMPNO), '')                                   AS campaign_number,
    NULLIF(TRIM(MAKETXT), '')                                  AS make,
    NULLIF(TRIM(MODELTXT), '')                                 AS model,
    TRY_CAST(NULLIF(YEARTXT, '9999') AS INTEGER)              AS model_year,
    NULLIF(TRIM(COMPNAME), '')                                 AS component,
    NULLIF(TRIM(MFGNAME), '')                                  AS manufacturer,
    TRY_CAST(strptime(NULLIF(RCDATE, ''), '%Y%m%d') AS DATE)  AS recall_date,
    TRY_CAST(strptime(NULLIF(ODATE, ''), '%Y%m%d') AS DATE)   AS owner_notified_date,
    TRY_CAST(POTAFF AS BIGINT)                                 AS potentially_affected,
    NULLIF(TRIM(RCLTYPECD), '')                                AS recall_type,
    NULLIF(TRIM(FMVSS), '')                                    AS fmvss_number,
    NULLIF(DESC_DEFECT, '')                                    AS defect_description,
    NULLIF(CONEQUENCE_DEFECT, '')                              AS defect_consequence,
    NULLIF(CORRECTIVE_ACTION, '')                             AS corrective_action,
    NULLIF(NOTES, '')                                          AS notes,
    DO_NOT_DRIVE                                               AS do_not_drive,
    PARK_OUTSIDE                                               AS park_outside
FROM "nhtsa-recalls"
WHERE RECORD_ID IS NOT NULL AND TRIM(RECORD_ID) <> ''
