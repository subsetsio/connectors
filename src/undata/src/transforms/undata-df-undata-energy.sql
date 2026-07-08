WITH casted AS (
    SELECT
        * EXCLUDE (OBS_VALUE),
        TRY_CAST(OBS_VALUE AS DOUBLE) AS obs_value
    FROM "undata-df-undata-energy"
)
SELECT * FROM casted
WHERE obs_value IS NOT NULL AND isfinite(obs_value)
