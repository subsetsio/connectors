SELECT DISTINCT
    CAST(name1 AS VARCHAR)                   AS name,
    NULLIF(CAST(name2 AS VARCHAR), '')       AS program_name,
    NULLIF(CAST(street1 AS VARCHAR), '')     AS street1,
    NULLIF(CAST(street2 AS VARCHAR), '')     AS street2,
    CAST(city AS VARCHAR)                    AS city,
    CAST(state AS VARCHAR)                   AS state,
    CAST(zip AS VARCHAR)                     AS zip,
    NULLIF(CAST(phone AS VARCHAR), '')       AS phone,
    NULLIF(CAST(intake1 AS VARCHAR), '')     AS intake_phone,
    NULLIF(CAST(website AS VARCHAR), '')     AS website,
    TRY_CAST(latitude AS DOUBLE)            AS latitude,
    TRY_CAST(longitude AS DOUBLE)           AS longitude,
    CAST(typeFacility AS VARCHAR)            AS facility_type
FROM "samhsa-findtreatment-facilities"
WHERE name1 IS NOT NULL AND CAST(name1 AS VARCHAR) <> ''
  AND state IS NOT NULL AND CAST(state AS VARCHAR) <> ''
