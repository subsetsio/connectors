SELECT
    TRY_CAST(CMPLID AS BIGINT)                                 AS complaint_id,
    TRY_CAST(ODINO AS BIGINT)                                  AS odi_number,
    NULLIF(TRIM(MFR_NAME), '')                                 AS manufacturer,
    NULLIF(TRIM(MAKETXT), '')                                  AS make,
    NULLIF(TRIM(MODELTXT), '')                                 AS model,
    TRY_CAST(NULLIF(YEARTXT, '9999') AS INTEGER)             AS model_year,
    NULLIF(TRIM(COMPDESC), '')                                 AS component,
    CRASH                                                      AS crash,
    FIRE                                                       AS fire,
    TRY_CAST(INJURED AS INTEGER)                              AS injured,
    TRY_CAST(DEATHS AS INTEGER)                               AS deaths,
    -- A handful of consumer-entered incident dates are impossible
    -- (e.g. year 2203); an incident cannot post-date "now", so drop those.
    CASE WHEN TRY_CAST(strptime(NULLIF(FAILDATE, ''), '%Y%m%d') AS DATE) <= current_date
         THEN TRY_CAST(strptime(NULLIF(FAILDATE, ''), '%Y%m%d') AS DATE)
    END                                                        AS incident_date,
    TRY_CAST(strptime(NULLIF(DATEA, ''), '%Y%m%d') AS DATE)   AS date_added,
    TRY_CAST(strptime(NULLIF(LDATE, ''), '%Y%m%d') AS DATE)   AS date_filed,
    NULLIF(TRIM(CITY), '')                                     AS city,
    NULLIF(TRIM(STATE), '')                                    AS state,
    TRY_CAST(MILES AS BIGINT)                                  AS miles,
    NULLIF(CDESCR, '')                                         AS description,
    NULLIF(TRIM(CMPL_TYPE), '')                                AS complaint_type,
    NULLIF(TRIM(PROD_TYPE), '')                                AS product_type
FROM "nhtsa-complaints"
WHERE CMPLID IS NOT NULL AND TRIM(CMPLID) <> ''
