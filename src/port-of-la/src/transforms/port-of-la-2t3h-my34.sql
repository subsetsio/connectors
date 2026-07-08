SELECT
    CAST(ei_year AS INTEGER) AS year,
    TRY_CAST(nox_tpy AS DOUBLE) AS nox_tpy,
    TRY_CAST(sox_tpy AS DOUBLE) AS sox_tpy,
    TRY_CAST(dpm_tpy AS DOUBLE) AS dpm_tpy
FROM "port-of-la-2t3h-my34"
WHERE ei_year IS NOT NULL
