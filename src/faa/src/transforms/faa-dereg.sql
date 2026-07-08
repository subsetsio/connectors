SELECT
    TRIM("N-NUMBER")                                      AS n_number,
    TRIM("SERIAL-NUMBER")                                 AS serial_number,
    TRIM("MFR-MDL-CODE")                                  AS mfr_mdl_code,
    TRIM("STATUS-CODE")                                   AS status_code,
    TRIM("NAME")                                          AS registrant_name,
    TRIM("CITY-MAIL")                                     AS city,
    TRIM("STATE-ABBREV-MAIL")                             AS state,
    TRIM("ZIP-CODE-MAIL")                                 AS zip_code,
    TRIM("COUNTRY-MAIL")                                  AS country,
    TRIM("ENG-MFR-MDL")                                   AS eng_mfr_mdl_code,
    TRY_CAST(NULLIF(TRIM("YEAR-MFR"), '') AS INTEGER)     AS year_mfr,
    TRIM("CERTIFICATION")                                 AS certification,
    TRY_STRPTIME(NULLIF(TRIM("AIR-WORTH-DATE"), ''), '%Y%m%d')::DATE AS air_worthiness_date,
    TRY_STRPTIME(NULLIF(TRIM("CANCEL-DATE"), ''), '%Y%m%d')::DATE    AS cancel_date,
    TRY_STRPTIME(NULLIF(TRIM("LAST-ACT-DATE"), ''), '%Y%m%d')::DATE  AS last_action_date,
    TRY_STRPTIME(NULLIF(TRIM("CERT-ISSUE-DATE"), ''), '%Y%m%d')::DATE AS cert_issue_date,
    TRIM("MODE-S-CODE")                                   AS mode_s_code,
    TRIM("MODE S CODE HEX")                               AS mode_s_code_hex
FROM "faa-dereg"
WHERE TRIM("N-NUMBER") <> ''
