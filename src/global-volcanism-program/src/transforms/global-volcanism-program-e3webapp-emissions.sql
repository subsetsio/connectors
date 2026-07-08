SELECT
    * EXCLUDE (Emission_ID, VolcanoNumber, SO2_Kilotons, StartDate, EndDate),
    TRY_CAST(Emission_ID AS BIGINT)        AS Emission_ID,
    TRY_CAST(VolcanoNumber AS BIGINT)      AS VolcanoNumber,
    TRY_CAST(SO2_Kilotons AS DOUBLE)       AS SO2_Kilotons,
    TRY_CAST(TRY_STRPTIME(StartDate, '%Y%m%d') AS DATE) AS StartDate,
    TRY_CAST(TRY_STRPTIME(EndDate, '%Y%m%d') AS DATE)   AS EndDate
FROM "global-volcanism-program-e3webapp-emissions"
