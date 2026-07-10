SELECT
    TRIM("N-NUMBER") AS n_number,
    TRIM("REGISTRANT") AS registrant,
    TRIM("STREET") AS street,
    TRIM("STREET2") AS street2,
    TRIM("CITY") AS city,
    TRIM("STATE") AS state,
    TRIM("ZIP CODE") AS zip_code,
    TRY_STRPTIME(NULLIF(TRIM("RSV DATE"), ''), '%Y%m%d')::DATE AS reserved_date,
    TRIM("TR") AS tr,
    TRY_STRPTIME(NULLIF(TRIM("EXP DATE"), ''), '%Y%m%d')::DATE AS expiration_date,
    TRIM("N-NUM-CHG") AS n_number_changed,
    TRY_STRPTIME(NULLIF(TRIM("PURGE DATE"), ''), '%Y%m%d')::DATE AS purge_date
FROM "faa-reserved"
WHERE TRIM("N-NUMBER") <> ''
