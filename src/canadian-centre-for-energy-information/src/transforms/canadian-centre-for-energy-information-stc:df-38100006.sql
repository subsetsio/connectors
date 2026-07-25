SELECT * EXCLUDE (DATAFLOW)
       REPLACE (TRY_CAST(OBS_VALUE AS DOUBLE) AS OBS_VALUE)
FROM "canadian-centre-for-energy-information-stc:df-38100006"
