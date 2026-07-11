SELECT
    date_name,
    TRY_CAST(nox_change_since_2005 AS DOUBLE) AS nox_change_since_2005,
    TRY_CAST(sox_change_since_2005 AS DOUBLE) AS sox_change_since_2005,
    TRY_CAST(dpm_change_since_2005 AS DOUBLE) AS dpm_change_since_2005
FROM "port-of-la-aiix-duyv"
WHERE date_name IS NOT NULL
