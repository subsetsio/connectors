SELECT * EXCLUDE (DATAFLOW)
       REPLACE (TRY_CAST(OBS_VALUE AS DOUBLE) AS OBS_VALUE)
FROM "canadian-centre-for-energy-information-ca1.rural:df-rural-12100138"
