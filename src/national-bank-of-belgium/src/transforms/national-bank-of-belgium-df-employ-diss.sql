SELECT
    * EXCLUDE (OBS_VALUE),
    TRY_CAST(OBS_VALUE AS DOUBLE) AS obs_value
FROM "national-bank-of-belgium-df-employ-diss"
WHERE TRY_CAST(OBS_VALUE AS DOUBLE) IS NOT NULL
