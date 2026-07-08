SELECT
    TRIM("CODE")                                          AS code,
    TRIM("MFR")                                           AS mfr,
    TRIM("MODEL")                                         AS model,
    TRIM("TYPE-ACFT")                                     AS type_aircraft,
    TRIM("TYPE-ENG")                                      AS type_engine,
    TRIM("AC-CAT")                                        AS aircraft_category,
    TRIM("BUILD-CERT-IND")                                AS build_cert_ind,
    TRY_CAST(NULLIF(TRIM("NO-ENG"), '') AS INTEGER)       AS num_engines,
    TRY_CAST(NULLIF(TRIM("NO-SEATS"), '') AS INTEGER)     AS num_seats,
    TRIM("AC-WEIGHT")                                     AS weight_class,
    TRY_CAST(NULLIF(TRIM("SPEED"), '') AS INTEGER)        AS cruising_speed,
    TRIM("TC-DATA-SHEET")                                 AS tc_data_sheet,
    TRIM("TC-DATA-HOLDER")                                AS tc_data_holder
FROM "faa-acftref"
WHERE TRIM("CODE") <> ''
